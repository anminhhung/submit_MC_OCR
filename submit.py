import cv2
import numpy as np
import re
import os
from collections import deque  
from sklearn.metrics.pairwise import cosine_similarity
import collections
from create_prices_proprocess_json import PRICES_PREPROCESS, PRICES_CHAR

with open("street.txt") as f:
    content = f.readlines()
LIST_STREET_DEF = [x.strip() for x in content] 

with open("seller.txt") as f:
    content = f.readlines()
LIST_SELLER_DEF = [x.strip() for x in content] 

with open("phone.txt") as f:
    content = f.readlines()
LIST_PHONE_DEF = [x.strip() for x in content] 

with open("prices.txt") as f:
    content = f.readlines()
LIST_PRICES_DEF = [x.strip() for x in content] 

with open("prices_prioritize.txt") as f:
    content = f.readlines()
LIST_PRICES_PRIORITIZE_DEF = [x.strip() for x in content] 

def draw_box(image, bbox, color=(0,0,255)):
    # pts = np.array([[xs_af[0],ys_af[0]],[xs_af[1],ys_af[1]],[xs_af[2],ys_af[2]],[xs_af[3],ys_af[3]]], np.int32)
    pts = np.array(bbox)
    pts = pts.reshape((-1,1,2))
    image = cv2.polylines(image,[pts],True, color)

    return image 

def draw_list_bbox(image, list_bbox):
    for bbox in list_bbox:
        # print(bbox)
        image = draw_box(image, bbox)
    
    return image

def get_list_bbox(file_path):
    with open(file_path) as f:
        content = f.readlines()

    list_bbox = []
    list_bbox_char = []
    list_bbox_str = []
    content = [x.strip() for x in content]
    for ele in content:
        bbox_str = ele.split(" ",8)[-1]
        ele = ele.split()
        i = 0
        bbox = []
        while(i<8):
            xs = int(ele[i])
            ys = int(ele[i+1])
            point = [xs, ys]
            bbox.append(point)

            i += 2
        
        bbox_char = ele[8:]
        list_bbox_char.append(bbox_char)
        list_bbox.append(bbox)
        list_bbox_str.append(bbox_str)
    
    return list_bbox, list_bbox_char, list_bbox_str

def search_day(input_string):
    result = re.search("^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$|^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$", input_string)
    if result == None:
        result = re.search("^\d\d\d\d/(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01]) (00|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9]):([0-9]|[0-5][0-9])$", input_string)

    return result

def get_center(bbox):
    center_x = (bbox[0][0] + bbox[2][0]) // 2
    center_y = (bbox[0][1] + bbox[2][1]) // 2
    return (center_x, center_y)

def draw_line(image, start_point, end_point):
    image = cv2.line(image, start_point, end_point, (0, 255, 255), 2)

    return image

def get_vector(point1, point2):
    vector = np.array([point2[0] - point1[0], point2[1] - point1[1]])
    vector = vector.reshape(1, 2)

    return vector

def compute_cosine(vector_bbox_prices, vector_gt):
    cosine = cosine_similarity(vector_bbox_prices, vector_gt)
    cosine = float(cosine[0][0])
    
    return cosine

def get_index_cosine(list_cosine, list_index_cosine):
    min_cosine = np.amax(list_cosine)
    index = np.where(list_cosine == min_cosine)
    index = index[0][0]
    index = list_index_cosine[index]
    return index

def get_day(list_bbox_char, list_bbox_str):
    list_number_prices = []
    index = None
    for i in range(len(list_bbox_char)):
        if len(list_bbox_str[i]) < 10: # > 1ty
            list_bbox_str[i] = list_bbox_str[i].replace(",", ".")
            list_number_prices.append(i)

        bbox = list_bbox_char[i]
        for content in bbox:
            result = search_day(content)
            if result != None:
                result = result.group()
                # print(list_bbox_str[i])
                index = i 
    
    return list_number_prices, index

def get_top_prices(list_number_prices, list_bbox_str, top=5):
    prices_top = deque([], top) # lấy top 1 trước có gì rồi sửa lại lấy top k 
    backup_arr = {}
    max_number = 0.0
    print(list_bbox_str)
    list_char_prices = ['d', 'đ', 'Đ', 'D', 'đồng']

    for i in list_number_prices:
        # prices = 0
        print("i: ", i)
        print("list_bbox_str[i]: ", list_bbox_str[i])
        try:
            # if list_bbox_str[i].find('.') == -1:
            #     continue
            
            prices = list_bbox_str[i]
            print("prices: ", prices)
            for char_price in list_char_prices:
                if prices.find(char_price) != -1:
                    prices = prices.replace(char_price, '')
                if prices.find(" ") != -1:
                    prices = prices.replace(" ", ".")

            prices = float(prices)

            if prices >= max_number:
                max_number = prices
                prices_top.append(i)
            else:
                if prices > 0:
                    backup_arr[i] = prices
        except Exception as e:
            print("bug in get top prices: ", e)
            pass # string not number!
        
    # them phan bu` cho du top5
    backup_arr = {k: v for k, v in sorted(backup_arr.items(), key=lambda item: item[1])}
    number_missed = top - len(prices_top)
    if number_missed > 0:
        i = 0
        for key, value in backup_arr.items():
            prices_top.append(key)
            i += 1
    print("prices top: ", prices_top)
    return prices_top

def get_prices(height_img, width_img, prices_box, list_bbox, list_bbox_str):
    # check parallel
    list_cosine = []
    list_index_cosine = []
    vector_gt = get_vector((0, height_img), (width_img, height_img))
    center_prices_bbox = get_center(prices_box)
    for i in range(len(list_bbox)):
        bbox = list_bbox[i]
        center_bbox = get_center(bbox)
        vector_bbox_prices = get_vector(center_bbox, center_prices_bbox)
        cosine = compute_cosine(vector_bbox_prices, vector_gt)
        list_cosine.append(cosine)
        list_index_cosine.append(i)
        # image = draw_line(image, center_box, center_prices_box)
        # image = draw_box(image, bbox, (255, 255, 0))
        
    bbox_index = get_index_cosine(list_cosine, list_index_cosine)

    return bbox_index

def get_index_street(list_bbox_str, number_line=4):
    list_street = []
    print(len(list_bbox_str))
    for i in range(number_line):
        content = list_bbox_str[i].lower()
        for word in LIST_STREET_DEF:
            if content.find(word) != -1:
                flag = False
                for char in LIST_PHONE_DEF:
                    if content.find(char) != -1:
                        flag = True 
                        break 
                if flag == False:
                    if i not in list_street:
                        list_street.append(i)
                        break

    return list_street

def get_index_name(list_bbox_str, number_line=4):
    for i in range(number_line):
        flag = False
        content = list_bbox_str[i].lower()
        for word in LIST_STREET_DEF:
            if content.find(word) != -1:
                flag = True
                break
        
        if flag == False:
            return i

def get_index_seller(list_bbox_str):
    for i in range(len(list_bbox_str)):
        content = list_bbox_str[i].lower()
        for word in LIST_SELLER_DEF:
            if content.find(word) != -1:
                return i

def get_submit_image(image_path, annot_path):
    output_dict = {}
    image = cv2.imread(image_path)

    height, width, channels = image.shape 

    list_bbox, list_bbox_char, list_bbox_str = get_list_bbox(annot_path)
    
    # get day
    list_number_prices, index_day_bbox = get_day(list_bbox_char, list_bbox_str)
    # day = list_bbox_str[index_day_bbox]
    # print(index_day_bbox)
    try:
        output_dict[index_day_bbox] = [list_bbox_str[index_day_bbox], 'TIMESTAMP']
    except:
        print("Not found index!")
        pass
    
    # get prices
    top_number = 10
    prices_top = get_top_prices(list_number_prices, list_bbox_str, top_number)
    try:
        flag_found = False
        for i in range(len(prices_top)):
            index_prices = prices_top[i]
            prices_box = list_bbox[index_prices]
            prices = list_bbox_str[index_prices]
            index_string_prices = get_prices(height, width, prices_box, list_bbox, list_bbox_str)
            
            prefix_raw = list_bbox_str[index_string_prices]
            prefix = prefix_raw.lower()
            #  kiem tra list prices uu tien
            flag = False
            print("prefix: ", prefix)
            print("prices: ", list_bbox_str[index_prices])
            for word in LIST_PRICES_PRIORITIZE_DEF:
                # print("prefix in PRIORITIZE: ", prefix)
                if prefix.find(word) != -1:
                    flag = True
                    break
            
            if flag==True:
                # preprocess
                tmp = False
                prices_value = list_bbox_str[index_prices]
                for key, value in PRICES_CHAR.items():
                    for ele in value:
                        index = prices_value.find(ele)
                        if index != -1:
                            tmp = True
                            prices_value = prices_value.replace(ele, key)
                            break

                    if tmp == True:
                        break

                print("########")
                print("prefix: ", prefix_raw)
                print("########")
                list_prefix = prefix_raw.split()
                for key, value in PRICES_PREPROCESS.items():
                    for ele in value:
                        for i in range(len(list_prefix)):
                            char = list_prefix[i]
                            if char == ele:
                                list_prefix[i] = key
                                break
                
                tmp = False
                prefix_raw = ' '.join(map(str, list_prefix))
                for key, value in PRICES_CHAR.items():
                    for ele in value:
                        index = prefix_raw.find(ele)
                        if index != -1:
                            tmp = True
                            prefix_raw = prefix_raw.replace(ele, key)
                            print("prefix: ", prefix_raw)
                            break
                            
                    if tmp == True:
                        break
                
                print("index prices: ", index_prices)
                prices = prefix_raw + '|||' + prices_value
                output_dict[index_prices] = [prefix_raw, 'TOTAL_COST']
                output_dict[index_prices*100] = [prices_value, 'TOTAL_COST']
                flag_found = True
                break
        
        if flag_found == False:
            for i in range(len(prices_top)):
                index_prices = prices_top[i]
                prices_box = list_bbox[index_prices]
                prices = list_bbox_str[index_prices]
                index_string_prices = get_prices(height, width, prices_box, list_bbox, list_bbox_str)
                
                prefix_raw = list_bbox_str[index_string_prices]
                prefix = prefix_raw.lower()
                # neu ko co trong list uu tien thi kiem tra list prices chung
                flag = False
                for word in LIST_PRICES_DEF:
                    # print("prefix in prices def: ", prefix)
                    if prefix.find(word) != -1:
                        flag = True
                        break
                
                if flag==True:
                    # preprocess
                    tmp = False
                    prices_value = list_bbox_str[index_prices]
                    for key, value in PRICES_CHAR.items():
                        for ele in value:
                            index = prices_value.find(ele)
                            if index != -1:
                                tmp = True
                                prices_value = prices_value.replace(ele, key)
                                break

                        if tmp == True:
                            break
                    print("########")
                    print("prefix: ", prefix_raw)
                    print("########")
                    list_prefix = prefix_raw.split()
                    for key, value in PRICES_PREPROCESS.items():
                        for ele in value:
                            for i in range(len(list_prefix)):
                                char = list_prefix[i]
                                if char == ele:
                                    list_prefix[i] = key
                                    break
                    
                    tmp = False
                    prefix_raw = ' '.join(map(str, list_prefix))
                    for key, value in PRICES_CHAR.items():
                        for ele in value:
                            index = prefix_raw.find(ele)
                            if index != -1:
                                tmp = True
                                prefix_raw = prefix_raw.replace(ele, key)
                                break
                                
                        if tmp == True:
                            break
                    print("index prices: ", index_prices)
                    prices = prefix_raw + '|||' + prices_value
                    output_dict[index_prices] = [prefix_raw, 'TOTAL_COST']
                    output_dict[index_prices*100] = [prices_value, 'TOTAL_COST']
                    break

    except Exception as e:
        print(e)
        print("Not found index!")
        pass

    # get street
    try:
        list_index_street = get_index_street(list_bbox_str)
        # street = ' '.join(list_street)
        # print(list_index_street)
        for index_street in list_index_street:
            output_dict[index_street] = [list_bbox_str[index_street], 'ADDRESS']
    except:
        print("Not found index!")
        pass

    # get name
    index_name = get_index_name(list_bbox_str)
    # print(index_name)
    try:
        output_dict[index_name] = [list_bbox_str[index_name], 'SELLER']
    except:
        print("Not found index!")
        pass

    # # get seller
    # index_seller = get_index_seller(list_bbox_str)
    # try:
    #     output_dict[index_seller] = [list_bbox_str[index_seller], 'SELLER']
    # except:
    #     print("Not found index!")
    #     pass

    # sort
    output_dict = collections.OrderedDict(sorted(output_dict.items()))

    return output_dict

def print_output(output_dict):
    list_value = []
    list_field = []
    for key, value in output_dict.items():
        list_value.append(value[0])
        list_field.append(value[1])
    
    result_value = '|||'.join(list_value)
    result_field = '|||'.join(list_field)
    
    return result_value, result_field

if __name__ == "__main__":
    name = "mcocr_public_145014rczsi"

    annot_path = os.path.join('result_txt', name+".txt")
    image_path = os.path.join('train_images', name+".jpg")

    output_dict = get_submit_image(image_path, annot_path)
    result_value, result_field = print_output(output_dict)
    print(result_value)
    print(result_field)

 