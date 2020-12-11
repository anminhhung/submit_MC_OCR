import cv2
import numpy as np
import re
from collections import deque  
from sklearn.metrics.pairwise import cosine_similarity
import collections

with open("street.txt") as f:
    content = f.readlines()
LIST_STREET_DEF = [x.strip() for x in content] 

with open("seller.txt") as f:
    content = f.readlines()
LIST_SELLER_DEF = [x.strip() for x in content] 

with open("phone.txt") as f:
    content = f.readlines()
LIST_PHONE_DEF = [x.strip() for x in content] 

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

def get_top_prices(list_number_prices, list_bbox_str, top=1):
    prices_top = deque([], top) # lấy top 1 trước có gì rồi sửa lại lấy top k 
    max_number = 0.0
    for i in list_number_prices:
        # print(list_bbox_str[i])
        prices = 0
        try:
            if list_bbox_str[i].find('.') == -1:
                continue
            prices = float(list_bbox_str[i])
        except:
            pass # string not number!
        if prices > max_number:
            max_number = prices
            prices_top.append(i)
    
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
    # bbox_result = list_bbox[bbox_index]

    # image = draw_box(image, bbox_result, (255, 255, 2))
    # image = draw_box(image, prices_box, (255, 255, 0))
    # cv2.imwrite("test.jpg", image)

    # str_prices = list_bbox_str[bbox_index]

    return bbox_index

def get_index_street(list_bbox_str, number_line=4):
    list_street = []
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
    output_dict[index_day_bbox] = list_bbox_str[index_day_bbox]
    
    # get prices
    prices_top = get_top_prices(list_number_prices, list_bbox_str, 1)
    index_prices = prices_top[0]
    prices_box = list_bbox[index_prices]
    prices = list_bbox_str[index_prices]
    index_string_prices = get_prices(height, width, prices_box, list_bbox, list_bbox_str)
    # prices = str_prices + " " + prices
    # print(index_prices)
    # print(index_string_prices)
    prices = list_bbox_str[index_string_prices] + " " + list_bbox_str[index_prices]
    output_dict[index_prices] = prices

    # get street
    list_index_street = get_index_street(list_bbox_str)
    # street = ' '.join(list_street)
    # print(list_index_street)
    for index_street in list_index_street:
        output_dict[index_street] = list_bbox_str[index_street]

    # get name
    index_name = get_index_name(list_bbox_str)
    # print(index_name)
    output_dict[index_name] = list_bbox_str[index_name]

    # get seller
    index_seller = get_index_seller(list_bbox_str)
    output_dict[index_seller] = list_bbox_str[index_seller]

    # sort
    output_dict = collections.OrderedDict(sorted(output_dict.items()))

    return output_dict

def print_output(output_dict):
    list_value = []
    for key, value in output_dict.items():
        list_value.append(value)
    
    result = '||| '.join(list_value)
    
    return result

if __name__ == "__main__":
    annot_path = "annot.txt"
    image_path = "image.jpg"

    output_dict = get_submit_image(image_path, annot_path)
    
    output = print_output(output_dict)
    print(output)