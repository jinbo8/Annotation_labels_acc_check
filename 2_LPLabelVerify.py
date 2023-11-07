import json
import os
import csv
import re


def check(json_label_path, writer, img_width=3840, img_height=2160):

    color = { "blue": (255, 0, 0),  # blue
              "green": (0, 128, 0),  # green
              "yellow": (0, 204, 255),  # yellow
              "white": (210, 210, 210),  # white
              "black": (0, 0, 0),  # black
              }

    type_all = ["car", "van", "truck", "bus", "heavy_truck", "bicycle", "cyclist", "tricycle"]
    pattern_ele = re.compile(r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使民军危临入应][A-HJ-NP-Z][A-HJ-NP-Z0-9险]{5}[A-HJ-NP-Z0-9挂学警港澳使领品]$')
    pattern_oil = re.compile(r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使民军危临入应][A-HJ-NP-Z][A-HJ-NP-Z0-9险]{4}[A-HJ-NP-Z0-9挂学警港澳使领品]$')

    # pattern=re.compile(r'^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z](([0-9]{5}[ADF])|([ADF]([A-HJ-NP??-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$')
    # file_name = re.compile(r'^R[0-9]\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu0[0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-000[0-9]{2}\.json$')
    # file_name=re.compile(r'^R[0-9]\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu0[0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-([0-5][0-9]|60)\_000\-000[0-9]{2}\.json$')
    # file_name = re.compile(r'^R10\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu[0-9][0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-([0-5][0-9]|60)\_000\-000[0-9]{2}\.json$')

    total_json = os.listdir(json_label_path)
    box2d_error = 0

    for i in range(len(total_json)):
        # if file_name.match(total_json[i])==None:
        #     writer.writerow([total_json[i], " ", "file_name error"])
        # print(total_json[i])
        if total_json[i].endswith("json"):

            # read json data
            json_path = os.path.join(json_label_path, total_json[i])
            json_file = open(json_path, 'r+', encoding='utf-8')
            annos = json.load(json_file,encoding='utf-8')
            # print(is_chinese(str(annos)))
            # print(f"annos:{annos}")


            plate = []
            error = 0

            for j in range(len(annos)):

                #  查找包含特定字符的车牌大图像
                # if "学" in annos[j]["plate_name"][0] or "警" in annos[j]["plate_name"][0] :
                #     print(annos[j]["plate_name"][0], json_path)
                # -------------- End -------------

                # 1.判断是否有"type"字段
                if annos[j].__contains__("type"):
                    type = annos[j]["type"].lower()
                    # 判断是否有 "type" 字段出现意外的名称
                    if type not in type_all:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "车辆类型错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有type这个主键"])

                # 2.判断"box2d"字段（1）是否缺失，（2）长度是否正常（3）数值是否越界
                if annos[j].__contains__("box2d"):
                    if len(annos[j]["box2d"]) == 4:
                        box = annos[j]["box2d"]
                        xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
                        # 判断bbox是否超过图片尺寸边界
                        if not (0 <= xmin < xmax <= img_width and 0 <= ymin < ymax <= img_height):
                            writer.writerow([json_path, f"第{j + 1}个车牌", "box2d数值错误，越界"])
                            error = 1
                            box2d_error += 1
                    else:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "box2d数目错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有box2d这个主键"])

                # 3.判断"corner"字段（1）是否缺失，（2）长度是否正常（3）数值是否越界
                if annos[j].__contains__("corner"):
                    if len(annos[j]["corner"]) == 8:
                        corner = annos[j]["corner"]
                        x1, y1, x2, y2, x3, y3, x4, y4 = corner[0], corner[1], corner[2], corner[3], corner[4], corner[5],  corner[6], corner[7]
                        if not (xmin <= x1 < x4 <= xmax or xmin <= x2 < x3 <= xmax or ymin <= y1 < y2 <= ymax or ymin <= y4 < y3 <= ymax):
                            writer.writerow([json_path, f"第{j + 1}个车牌", "plate not in box"])
                        elif (min(x1, x2) - xmin) > 6 or (xmax - max(x3, x4)) > 5 or (min(y1, y4) - ymin) > 5 or (ymax - max(y2, y3)) > 5:
                            writer.writerow([json_path, f"第{j + 1}个车牌", "标注框误差超过三个像素"])
                    else:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "corner角点坐标数量错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有corner这个主键"])

                # 4.判断是否有"plate_color"字段缺失
                if annos[j].__contains__("plate_color"):
                    plate_color = annos[j]["plate_color"]
                    keys = color.keys()
                    if plate_color not in keys:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "plate_color错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "plate_color"])

                # 5.判断是否有"plate_number"字段缺失
                if annos[j].__contains__("plate_name"):
                    plate_name = annos[j]["plate_name"][0]
                    plate_layer = annos[j]["plate_layer"]
                    plate_color = annos[j]["plate_color"]

                    if plate_color == "green":
                        if not pattern_ele.match(plate_name):
                            plate_name_Aa = plate_name.upper()
                            plate_name_blank = plate_name.replace(" ",'')
                            if len(plate_name_blank) != len(plate_name):
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格：{plate_name}"])
                            if plate_name_Aa != plate_name:
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母：{plate_name}"])
                        if len(plate_name)!=8:
                            writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号or颜色错误：{plate_color}-{plate_name}"])

                    if plate_color == "yellow":
                        if plate_layer == "double":
                            if not pattern_ele.match(plate_name):
                                plate_name_Aa = plate_name.upper()
                                plate_name_blank = plate_name.replace(" ",'')
                                if len(plate_name_blank) != len(plate_name):
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格：{plate_name}"])
                                if plate_name_Aa != plate_name:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母：{plate_name}"])
                            if len(plate_name) != 8:
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号or颜色错误：{plate_color}-{plate_name}"])
                        if plate_layer == "single":
                            if not pattern_ele.match(plate_name):
                                plate_name_Aa = plate_name.upper()
                                plate_name_blank = plate_name.replace(" ", '')
                                if len(plate_name_blank) != len(plate_name):
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格：{plate_name}"])
                                if plate_name_Aa != plate_name:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母：{plate_name}"])
                            if len(plate_name) != 7:
                                writer.writerow(
                                    [json_path, f"第{j + 1}个车牌", f"车牌号or颜色错误：{plate_color},{plate_name}"])
                        if plate_layer not in ["single", "double"]:
                            writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌颜色字符错误：{plate_color}"])

                    if plate_color in ["blue", "white", "black"]:
                        if not pattern_oil.match(plate_name):
                            plate_name_Aa = plate_name.upper()
                            plate_name_blank = plate_name.replace(" ", '')
                            if not len(plate_name_blank) == len(plate_name):
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格:{plate_name}"])
                            if not plate_name_Aa == plate_name:
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母:{plate_name}"])
                            if len(plate_name_blank) != 7:
                                writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号or颜色错误：{plate_color}-{plate_name}"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有plate_name主键"])

                # 6.判断是否有"plate_layer"字段缺失, 单双层字段是否正确，
                if annos[j].__contains__("plate_layer"):
                    plate_layer = annos[j]["plate_layer"]
                    plate_number = annos[j]["plate_name"]
                    if plate_layer == "double":
                        if "_" not in plate_number[0]:
                            writer.writerow([json_path, f"第{j + 1}个车牌",f"plate_layer错误,双层要有下划线,plate_layer：{plate_layer},{plate_number}"])
                    elif plate_layer == "single":
                        if "_" in plate_number[0]:
                            writer.writerow([json_path, f"第{j + 1}个车牌", f"plate_layer or plate_number错误,{plate_layer},{plate_number}"])
                    else:
                        writer.writerow([json_path, f"第{j + 1}个车牌", f"plate_layer不合法，plate_layer：{plate_layer}"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有plate_layer主键"])

            if not len(plate) == len(set(plate)):
                writer.writerow([json_path, " ", f"该图片车牌号重复：{plate}"])


def check_license_plate_label(json_label_path, res_csv_path, img_width=3840, img_height=2160):

    with open(res_csv_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow([" ", "车牌id", "错误类型"])
        check(json_label_path, writer, img_width=3840, img_height=2160)


if __name__ == "__main__":
    json_label_path = "/home/dell/桌面/linchao/TS_2D_车牌标注_20230921(1)/TS_2D_车牌标注_20230921/a24"
    res_csv_path = "/home/dell/桌面/linchao/res/run_json.csv"

    check_license_plate_label(json_label_path, res_csv_path, img_width=3840, img_height=2160)