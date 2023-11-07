
import json
import os
import csv
import re
import unicodedata


# 对于车牌颜色，按照车牌颜色比例最高的颜色进行标注，例如蓝牌为0、绿牌为1、黄牌为2、白牌为3、黑牌为4。
# 在标注车牌层数时，无牌车车牌类型标注为0、单层车牌标注为1、双层车牌标注为2。

def check(json_dir):
    color = {"0": (255, 255, 0), "1": (0, 128, 0), "2": (0, 165, 255), "3": (255, 255, 255), "4": (255, 255, 255),
             "5": (255, 255, 255)}
    type_all = ["car", "truck", "heavy_truck", "van", "bus", "motorbike", "other"]
    pattern_oil = re.compile(r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]$')
    pattern_elc = re.compile(r'^([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-HJ-NP-Z][A-HJ-NP-Z0-9]{5}[A-HJ-NP-Z0-9挂学警港澳使领])$')
    pattern=re.compile(r'^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z](([0-9]{5}[ADF])|([ADF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$')

    file_name = re.compile(r'^R[0-9]\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu0[0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-000[0-9]{2}\.json$')
    # file_name=re.compile(r'^R[0-9]\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu0[0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-([0-5][0-9]|60)\_000\-000[0-9]{2}\.json$')
    # file_name = re.compile(r'^R10\_[A-Z][a-z]\_Cam[SNWE]{1}\_101\_gpu[0-9][0-9]\_2022\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[01])\-([01][0-9]|2[0-4])\-([0-5][0-9]|60)\-([0-5][0-9]|60)\_000\-000[0-9]{2}\.json$')

    total_json = os.listdir(json_dir)
    print(json_dir)
    box2d_error=0


    for i in range(len(total_json)):
        if file_name.match(total_json[i])==None:
            writer.writerow([total_json[i], " ", "file_name error"])

        print(total_json[i])
        if not total_json[i].endswith("_1.json"):
            json_path = os.path.join(json_dir, total_json[i])
            json_file = open(json_path, 'r+',encoding='utf-8')
            print(json_file)
            annos = json.load(json_file,encoding='utf-8')
            print(json_file)
            # print(is_chinese(str(annos)))
            plate = []
            error=0



            for j in range(len(annos)):

                if annos[j].__contains__("type"):
                    type = annos[j]["type"].lower()
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有type这个主键"])

                if annos[j].__contains__("box2d"):
                    if len(annos[j]["box2d"])==4:
                            box = annos[j]["box2d"]
                            xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
                            if not (0 <= xmin < xmax <= 3840 and 0 <= ymin < ymax <= 2160):
                                writer.writerow([json_path, f"第{j + 1}个车牌", "box2d错误"])
                                error = 1
                                box2d_error += 1
                    else:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "box2d数目错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有box2d这个主键"])

                if annos[j].__contains__("corner"):
                    if len(annos[j]["corner"])==8:
                        corner = annos[j]["corner"]
                        x1, y1, x2, y2, x3, y3, x4, y4 = corner[0], corner[1], corner[2], corner[3], corner[4], corner[5], \
                                                         corner[6], corner[7]
                        if not (
                                xmin <= x1 < x4 <= xmax or xmin <= x2 < x3 <= xmax or ymin <= y1 < y2 <= ymax or ymin <= y4 < y3 <= ymax):
                            writer.writerow([json_path, f"第{j + 1}个车牌", "plate not in box"])
                        # elif (min(x1, x2) - xmin) > 3 or (xmax - max(x3, x4)) > 3 or (min(y1, y4) - ymin) > 3 or (
                        #         ymax - max(y2, y3)) > 3:
                        #     writer.writerow(
                        #         [json_path, f"第{j + 1}个车牌", "标注框误差超过三个像素"])
                        #     error = 1
                        #     corner_error += 1
                        #
                        # writer.writerow([json_path, f"第{j + 1}个车牌", "标注框误差超过三个像素"])
                    else:
                        writer.writerow([json_path, f"第{j + 1}个车牌", "corner数目错误"])
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "没有corner这个主键"])


                if annos[j].__contains__("plate_color"):
                    plate_color = annos[j]["plate_color"]
                else:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "plate_color"])

                if type not in type_all:
                    writer.writerow([json_path, f"第{j + 1}个车牌", "车辆类型错误"])

                if annos[j].__contains__("plate_number"):
                    plate_number = annos[j]["plate_number"]
                    plate_color = annos[j]["plate_color"]
                    if plate_number != "null":
                        if plate_color == "0":
                            if not pattern_oil.match(plate_number):
                                plate_number_Aa = plate_number.upper()
                                plate_number_blank = plate_number.replace(" ",'')
                                if len(plate_number_blank) != len(plate_number):
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格--{plate_number}"])
                                if  plate_number_Aa != plate_number:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母--{plate_number}"])
                                else:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号错误--颜色：{plate_color}--{plate_number}"])
                        elif plate_color == "1":
                            if not pattern_elc.match(plate_number):
                                plate_number_Aa = plate_number.upper()
                                plate_number_blank = plate_number.replace(" ", '')
                                if not len(plate_number_blank) == len(plate_number):
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格--{plate_number}"])
                                if not plate_number_Aa == plate_number:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母--{plate_number}"])
                                else:
                                    writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号错误--颜色：{plate_color}--{plate_number}"])
                        # plate_number_Aa=plate_number.upper()
                        # plate_number_blank=plate_number.replace(" ",'')
                        # if not len(plate_number_blank)==len(plate_number):
                        #     writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有空格--{plate_number}"])
                        # if not plate_number_Aa==plate_number:
                        #     writer.writerow([json_path, f"第{j + 1}个车牌", f"车牌号有小写字母--{plate_number}"])

                        #

                    # if annos[j].__contains__("plate_layer"):
                    #     plate_layer = annos[j]["plate_layer"]
                    #     plate_number = annos[j]["plate_number"]
                    #     type = annos[j]["type"]
                    #     if plate_layer == "2":
                    #         if len(plate_number)>4 and plate_number[2] != "_":
                    #             writer.writerow([json_path, f"第{j + 1}个车牌",f"plate_layer错误,双层要有下划线,plate_layer={plate_layer}--{plate_number}--{type}"])
                    #     elif plate_layer=="1":
                    #         pass
                    #     elif plate_layer=="null" or plate_layer=="0":
                    #         if not plate_number=="null":
                    #             writer.writerow([json_path, f"第{j + 1}个车牌",
                    #                              f"plate_layer错误,空车牌层数为0，plate_layer={plate_layer}--{plate_number}--{type}"])
                    #     elif plate_layer=="0":
                    #         writer.writerow([json_path, f"第{j + 1}个车牌",
                    #                          f"plate_layer错误,不合法，plate_layer={plate_layer}--{plate_number}--{type}"])

                    if type not in ["truck", "heavy_truck"]:
                        if plate_number != "null":
                            plate.append(plate_number)
                    # else:
                    #     writer.writerow([json_path, f"第{j + 1}个车牌", "plate_number"])

            if not len(plate) == len(set(plate)):
                writer.writerow([json_path, " ", f"该图片车牌号重复{plate}"])



if __name__ == "__main__":
    # json_path = "C:/Users/admin/Desktop/车牌数据/test_samples"

    json_path = "F:/batch1_json_png/batch1_json2.0/batch1_json_查收"
    with open("F:/batch1_json_png/batch1_json2.0/batch1_json.csv", "w",newline='') as csvfile:
        writer = csv.writer(csvfile)

        # 先写入columns_name
        writer.writerow([" ", "车牌id", "错误类型"])
        check(json_path)
