# -*- coding: utf-8 -*-

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import pandas as pd
import json
import math

with open("package.json", 'r', encoding='utf-8') as f:
    j = json.load(f)


class SongList:
    def __init__(self):
        self.png_filename = "./template/" + j["png_filename"]
        self.bk_image = "./data/test.jpg"
        self.font_style = j["font_style"]
        self.table_name = j["file_name"]
        self.title = j["title"]
        self.title_color = (j["font_color_1"], j["font_color_2"], j["font_color_3"])
        self.title_size = j["title_size"]
        self.font_en_style = j["font_en_style"]
        self.font_color = (j["font_color_1"], j["font_color_2"], j["font_color_3"])
        self.font_size = j["font_size"]
        self.num1 = j["1_num"]
        self.num2 = j["2_num"]
        self.num3 = j["3_num"]
        self.num4 = j["4_num"]
        self.num5 = j["5_num"]
        self.num10 = j["10_num"]
        self.num999 = j["999_num"]
        self.height = 0
        self.width = 0

    def cut_image(self):
        """
        :return: 裁剪图片
        """
        png_filename = self.png_filename
        big_image = Image.open(png_filename)
        # print(big_image.size)

        self.height = big_image.size[1]
        self.width = big_image.size[0]
        print(self.height, self.width)

        size_times = 1440 / self.width
        self.width = 1440
        self.height = int(self.height * size_times)
        big_image.resize((self.width, self.height), Image.ANTIALIAS).save(self.bk_image)
        # big_image

        # box = (0, 170, 1440, 2880)  # 将要裁剪的图片块距原图左边界距左边距离，上边界距上边距离，右边界距左边距离，下边界距上边的距离。
        # rect_on_big = big_image.crop(box)
        # rect_on_big.save(self.bk_image)

    def image_writer(self, data):
        # 编辑图片路径
        bk_img = cv2.imread(self.bk_image)
        # 设置需要显示的字体
        # font_path = self.font_path
        font = ImageFont.truetype(self.font_style, self.font_size)
        font_en = ImageFont.truetype(self.font_en_style, self.font_size)
        title_font = ImageFont.truetype(self.font_style, self.title_size)
        img_pil = Image.fromarray(bk_img)
        print(img_pil.width, img_pil.height)
        draw = ImageDraw.Draw(img_pil)
        draw.text((self.width / 10, self.height / 20), self.title, font=title_font, fill=self.font_color)
        print(data)
        for row in data:
            if row['is_en'] is True:
                draw.text((row['x_int'], row['y_int']), row['name'], font=font, fill=self.font_color)
            else:
                draw.text((row['x_int'], row['y_int']), row['name'], font=font_en, fill=self.font_color)
        bk_img = np.array(img_pil)
        cv2.imshow("./data/add_text", bk_img)
        cv2.waitKey()
        cv2.imwrite("./result/song_list.jpg", bk_img)

    @staticmethod
    def en_sep(x):
        if x["is_en"] is False:
            if x["length"] > 18:
                return 999
            else:
                return 888
        else:
            return x["length"]

    @staticmethod
    def is_contains_chinese(strs):
        """
        检验是否包含汉字
        :param strs:
        :return:
        """
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    def read_data(self):
        """
        读取歌曲清单对应长度
        :return:
        """
        df = pd.read_csv(self.table_name, encoding='ANSI')
        df.drop_duplicates(inplace=True)
        df['name'] = df['name'].str.strip()
        df["length"] = df["name"].apply(lambda x: len(x.strip('').strip("*")))
        df["is_en"] = df["name"].apply(lambda x: self.is_contains_chinese(x))
        # df["length_new"] = df[["is_en", "length"]].apply(lambda x: 999 if x["is_en"] is False else x["length"], axis=1)
        df["length_new"] = df[["is_en", "length"]].apply(lambda x: self.en_sep(x), axis=1)
        df.sort_values(by="length_new", ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['count'] = df.groupby('length_new')['name'].transform('count')
        df['each_row'] = df['length_new'].apply(self.each_row)
        # df['row_loc'] = df.index % df['each_row']
        df['num1'] = 1
        df['row_num'] = df.groupby('length_new')['num1'].transform('cumsum')
        # df['row_num1'] = math.ceil(df['row_num']/df['each_row'])
        df['row_num1'] = df[['row_num', 'each_row']].apply(lambda x: math.ceil(x['row_num'] / x['each_row']), axis=1)
        # data = json.loads(df.to_json(orient="records", force_ascii=False))
        data = df.to_dict(orient="records")
        return data

    @staticmethod
    def reset_row(data):
        data[0]["row_num2"] = 1
        for i in range(1, len(data)):
            if (data[i]['row_num1'] != data[i - 1]['row_num1']) and (
                    data[i]['length_new'] == data[i - 1]['length_new']):
                data[i]["row_num2"] = data[i - 1]["row_num2"] + 1
            elif data[i]['length_new'] != data[i - 1]['length_new']:
                data[i]["row_num2"] = data[i - 1]["row_num2"] + 2
            else:
                data[i]["row_num2"] = data[i - 1]["row_num2"]
        row_loc = 0
        data[0]['row_loc'] = 0
        for j in range(1, len(data)):
            if (row_loc < data[j]['each_row']) and (data[j]['row_num2'] == data[j - 1]['row_num2']):
                row_loc += 1
            else:
                row_loc = 0
            data[j]['row_loc'] = row_loc
        return data

    def make_data(self, data):
        df = pd.DataFrame(data)
        # width = 1440 - 200
        # height = 2700 - 300 - 200
        width = self.width * 14 / 15
        height = self.height * 11 / 13

        width0 = self.width * 1 / 14
        height0 = self.height * 1 / 10
        df['x_step'] = width / df['each_row']
        df['y_step'] = height / df['row_num2'].max()

        df['x'] = width0 + df['row_loc'] * df['x_step']
        df['y'] = height0 + (df['row_num2'] - 1) * df['y_step']
        df['x_int'] = df['x'].apply(lambda x: int(x))
        df['y_int'] = df['y'].apply(lambda y: int(y))
        data = json.loads(df.to_json(orient="records", force_ascii=False))
        return data

    # def each_row(self, num):
    #     if num == 1:
    #         return self.num1
    #     elif num == 2:
    #         return self.num2
    #     elif num == 3:
    #         return self.num3
    #     elif num == 4:
    #         return self.num4
    #     elif num == 5:
    #         return self.num5
    #     elif num == 999:
    #         return self.num999
    #     elif 8 <= num < 12:
    #         return self.num10
    #     else:
    #         return 3

    def each_row(self, num):
        num_mapping = {
            1: self.num1,
            2: self.num2,
            3: self.num3,
            4: self.num4,
            5: self.num5,
            999: self.num999,
        }

        if 8 <= num < 12:
            return self.num10
        else:
            return num_mapping.get(num, 3)

    def run(self):
        self.cut_image()

        data = self.read_data()
        data = self.reset_row(data)
        data = self.make_data(data)

        df1 = pd.DataFrame(data)
        df1.to_excel('result.xlsx')
        self.image_writer(data)


if __name__ == '__main__':
    print('歌单生成工具_by慕少艾')
    songlist = SongList()
    songlist.run()
    # songlist.cut_image()
