import re 

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


list_bbox, list_bbox_char, list_bbox_str = get_list_bbox('result_txt/mcocr_val_145114anqqj.txt')

cnt_max = 0
date_str = ''
for i in range(len(list_bbox_str)):
    string = list_bbox_str[i]
    cnt = string.count('-')
    if cnt > cnt_max:
        cnt_max = cnt
        if cnt >= 2:
            date_str = string

print(date_str)