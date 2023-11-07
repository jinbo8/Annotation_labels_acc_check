import json
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def select(json_dir, img_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 可自行修改显示颜色

    color = { "blue": (255, 0, 0),  # blue
              "green": (0, 128, 0),  # green
              "yellow": (0, 204, 255),  # yellow
              "white": (210, 210, 210),  # white
              "black": (0, 0, 0),  # black
              }

    total_json = os.listdir(json_dir)
    for i in range(len(total_json)):
        if total_json[i].endswith("json"):

            # load json label
            json_path = os.path.join(json_dir, total_json[i])
            json_file = open(json_path, encoding='utf-8')
            annos = json.load(json_file)

            # print(f"annos:{annos}")

            # read image
            img_path = img_dir + "/" + total_json[i][:-4] + "jpg"
            img = cv2.imread(img_path)

            for j in range(len(annos)):
                print(f" annos[j].keys():{annos[j].keys()}")
                if "type" in annos[j].keys():
                    type = annos[j]["type"]
                if  "box2d" in annos[j].keys():
                    box = annos[j]["box2d"]
                if "plate_color" in annos[j].keys():
                    plate_color = annos[j]["plate_color"]
                if "plate_number" in annos[j].keys():
                    plate_number = annos[j]["plate_number"]
                if "plate_layer" in annos[j].keys():
                    plate_layer = annos[j]["plate_layer"]
                if "plate_name" in annos[j].keys():
                    plate_name = annos[j]["plate_name"]


                if "type" not in annos[j].keys():
                    type = ' '
                if "box2d" not in annos[j].keys():
                    box = ' '
                if "plate_color" not in annos[j].keys():
                    plate_color = ' '
                if "plate_number" not in annos[j].keys():
                    plate_number = ' '
                if "plate_layer" not in annos[j].keys():
                    plate_layer = ' '
                if "plate_name" not in annos[j].keys():
                    plate_name = ' '
                # print(f"plate_name:{plate_name}")
                if len(box)==4:
                    xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color[plate_color], thickness=2)  # 画车牌矩形框到图上

                # print(plate_number)

                # # 画车牌上方填充框和字符
                cv2.rectangle(img, (xmin, ymin), (xmin + 350, ymin - 30), color[plate_color], -1, cv2.LINE_AA)
                info = type +plate_number +' '+plate_layer+' '+plate_name[0] + ' '+plate_color
                img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 图像从OpenCV格式转换成PIL格式
                font = ImageFont.truetype('字体/JDJHCU.ttf', 22)  # 40为字体大小，根据需要调整?
                draw = ImageDraw.Draw(img_pil)
                draw.text((xmin, ymin-30), info, font=font, fill=(0, 0, 0))

                # 画车牌 corner point 到图上
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

    json_path = "/home/dell/桌面/linchao/json"
    img_path = "/home/dell/桌面/linchao/img"
    output_path = img_path + "_res"

    select(json_path, img_path, output_path)
