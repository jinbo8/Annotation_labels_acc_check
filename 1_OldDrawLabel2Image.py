#!/usr/bin/python
# coding: utf-8
# @File    : show_plate_anno.py
# @Time    : 2022/10/28 11:17
# @Author  : Zhang Li
# @Email   : lizhang671@gmail.com

import json
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def select(json_dir, img_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    color = {"0": (255, 255, 0),
             "1": (0, 128, 0),
             "2": (0, 165, 255),
             "3": (255, 255, 255),
             "4": (255, 255, 255),
             "5": (255, 255, 255),
             "null": (133, 108, 252)
             }
    total_json = os.listdir(json_dir)
    for i in range(len(total_json)):
        if total_json[i].endswith("json"):
            if not total_json[i].endswith("_1.json"):
                json_path = os.path.join(json_dir, total_json[i])
                json_file = open(json_path, encoding='utf-8')
                print(json_file)
                annos = json.load(json_file)
                img_path = img_dir + "/" + total_json[i][:-4] + "png"
                img = cv2.imread(img_path)
                for j in range(len(annos)):
                    type = annos[j]["type"]
                    box = annos[j]["box2d"]
                    plate_color = annos[j]["plate_color"]
                    plate_number = annos[j]["plate_number"]
                    xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color[plate_color], thickness=2)
                    cv2.rectangle(img, (xmin, ymin), (xmin + 210, ymin - 30), color[plate_color], -1, cv2.LINE_AA)
                    # print(plate_number)
                    info = type + " " + plate_number
                    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 图像从OpenCV格式转换成PIL格式
                    font = ImageFont.truetype('C:/Users/admin/Desktop/车牌数据/字体/JDJHCU.ttf', 22)  # 40为字体大小，根据需要调整?
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((xmin, ymin-30), info, font=font, fill=(0, 0, 0))
                    img = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)
                    corner = annos[j]["corner"]
                    x1, y1, x2, y2, x3, y3, x4, y4 = int(corner[0]), int(corner[1]), int(corner[2]), int(corner[3]), int(corner[4]), int(corner[5]), int(corner[6]), int(corner[7])
                    cv2.line(img, (x1, y1), (x2, y2), (60, 20, 220), 2)
                    cv2.line(img, (x2, y2), (x3, y3), (60, 20, 220), 2)
                    cv2.line(img, (x3, y3), (x4, y4), (60, 20, 220), 2)
                    cv2.line(img, (x1, y1), (x4, y4), (60, 20, 220), 2)
                img_output_path = output_dir + "/" + total_json[i][:-5] + ".jpg"
                cv2.imwrite(img_output_path, img)


if __name__ == "__main__":
    # json_path = "C:/Users/admin/Desktop/json"
    # img_path = "C:/Users/admin/Desktop/img"
    json_path = "F:/batch3/batch3_json"
    img_path = "F:/batch3/batch3"
    output_path = img_path + "_json_20221110"
    select(json_path, img_path, output_path)
