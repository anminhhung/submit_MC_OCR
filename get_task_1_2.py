import requests
import json
import matplotlib as plt
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os


def output_txt(data_task1, data_task2, output_path):
    bboxs = data_task1['result']
    words = data_task2['result']
    # print(words)
    result_txt_list = ''
    for box, word in zip(bboxs, words):
        result_txt_line = ''
        box = box['bbox']
        word = word['words']
        # print(box)
        # print(word)
        for b in box:
            result_txt_line += str(b) + ' '
            # print(result_txt_line)
        result_txt_line += str(word)
        result_txt_list += result_txt_line + '\n'
    with open(output_path, 'w') as out:
        out.write(result_txt_list)
        print('output_path: ',output_path, '----ok----')

TASK1_URL = 'http://service.mmlab.uit.edu.vn/receipt/task1/predict'
TASK2_URL = 'http://service.mmlab.uit.edu.vn/receipt/task2/predict'
OUTPUT = 'output_img'



if __name__ == "__main__":
    name = "mcocr_val_145115czygu"

    annot_path = os.path.join('result_txt', name+".txt")
    img_path = os.path.join('upload', name+".jpg")

    print(img_path)

    img = cv2.imread(img_path)

    detect_task1 = requests.post(TASK1_URL, files={"file": (
        "filename", open(img_path, "rb"), "image/jpeg")}).json()



    files = [
        ("file", ("filename", open(img_path, "rb"), "image/jpeg")),
        ('data', ('data', json.dumps(detect_task1), 'application/json')),
    ]


    detect_task2 = requests.post(TASK2_URL, files=files).json()
    print(detect_task2)

    # output_txt_file = os.path.join(OUTPUT, img_path.split('.')[0] + '.txt')

    output_txt(detect_task1, detect_task2, "output.txt")