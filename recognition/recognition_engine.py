# -*- coding: utf-8 -*-
from recognition.image_processing import ImageProcessing
import os
import re
import time
import pytesseract


class RecognitionEngine():
    """敏感信息识别引擎"""
    def __init__(self, img_name, sub_imgs, vocabulary_path):
        """初始化参数"""
        self.img_name = img_name
        self.sub_imgs = sub_imgs
        self.vocabulary_path = vocabulary_path
        
    def build_vocabulary(self):
        """建立敏感信息库"""
        vocabulary = []
        with open(self.vocabulary_path, 'r') as f:
            while True:
                line = f.readline().split('\n')[0]
                if not line:
                    break
                else:
                    vocabulary.append(line)
        return vocabulary
    
    def get_character(self,):
        """提取字符"""
        character = []
        for sub_img in self.sub_imgs[self.img_name]:
            text = pytesseract.image_to_string(sub_img, lang='chi_sim', config='-psm 6')
            re_text = re.sub('[^\u4e00-\u9fa5a-zA-Z]+', ' ', text).replace('_', ' ')    # 过滤非中英文字符
            if len(re_text) >= 2:
                clean_text = re_text.lower().strip().split(' ')
                character.extend(clean_text)
        return character

    def recognizer(self):
        """识别器"""
        sensitive_vocabulary = self.build_vocabulary()
        character = self.get_character()
        for char in character:
            if char in sensitive_vocabulary:
                return "含敏感信息: {:}".format(char)
        for char in character:
            if char in ''.join(sensitive_vocabulary) and len(char) > 1:
                return "含敏感信息: {:}".format(char)
        return None


if __name__ == '__main__':
    imgs_path = '/users/vita/desktop/test3'
    vocabulary_path = '/users/vita/pycharmprojects/images_review_projects/recognition/sensitive_vocabulary'
    imgs_name = os.listdir(imgs_path)
    result = {}
    result_time = {}
    if '.DS_Store' in imgs_name:
        imgs_name.remove('.DS_Store')
    for img_name in imgs_name:
        since = time.time()
        img_path = os.path.join(imgs_path, img_name)
        processing_engine = ImageProcessing(img_name, img_path)
        sub_imgs = processing_engine.get_tailored_img()
        recognition_engine = RecognitionEngine(img_name, sub_imgs, vocabulary_path)
        sensitive_information = recognition_engine.recognizer()
        if sensitive_information:
            result[img_name] = sensitive_information
        result_time[img_name] = time.time() - since


    """
    result = {'机油散热器0.jpg': '含敏感信息: 三',
              '前大灯总成（右）60.jpg': '含敏感信息: 妻',
              '喷油嘴1.jpg': '含敏感信息: 安',
              '发电机10.jpg': '含敏感信息: 厂',
              '空调泵44.jpg': '含敏感信息: 厂',
              '档位开关（自动）1.jpg': '含敏感信息: 坦克',
              '发动机电脑3.jpg': '含敏感信息: 毛泽',
              '点火开关座0.jpg': '含敏感信息: 韩',
              '龙门架总成1.jpg': '含敏感信息: 龟',
              '节气门总成0.jpg': '含敏感信息: 三',
              '后保险杠皮43.jpg': '含敏感信息: 暴',
              '发电机39.jpg': '含敏感信息: 三',
              '点火线圈2.jpg': '含敏感信息: 三',
              '变速器滤清器3.jpg': '含敏感信息: 门',
              '点火线圈10.jpg': '含敏感信息: 让',
              '前大灯近光灯泡（右）4.jpg': '含敏感信息: 厂',
              '倒车镜半总成（左）8.jpg': '含敏感信息: 三',
              '倒车镜半总成（右）5.jpg': '含敏感信息: 天安',
              '后制动鼓（右）2.jpg': '含敏感信息: 厂',
              '空气流量计23.jpg': '含敏感信息: 三',
              '后减震器总成（左）0.jpg': '含敏感信息: 韩',
              '低音喇叭5.jpg': '含敏感信息: 女优',
              '倒车镜转向灯（右）0.jpg': '含敏感信息: 习',
              '变速箱机脚胶（左）3.jpg': '含敏感信息: 习',
              '点火开关座3.jpg': '含敏感信息: 灯',
              '倒车镜总成（左）11.jpg': '含敏感信息: zi',
              '点火线圈13.jpg': '含敏感信息: 妻',
              '后门外拉手（右）3.jpg': '含敏感信息: 广',
              '鼓风机调速模块5.jpg': '含敏感信息: 八'}
              
    result = {'发电机10.jpg': '含敏感信息: 爱液',
              '中网20.jpg': '含敏感信息: 肉棒',
              '方向机内球头（右）0.jpg': '含敏感信息: mother',
              '变速器电脑3.jpg': '含敏感信息: ll',
              '后保险杠皮78.jpg': '含敏感信息: pussy',
              '后门饰板（左）1.jpg': '含敏感信息: 采购',
              '车外温度传感器2.jpg': '含敏感信息: 汽配',
              '前大灯半总成（左）93.jpg': '含敏感信息: 汽配',
              '变速箱油8.jpg': '含敏感信息: eb',
              '变速箱油6.jpg': '含敏感信息: ve'}
              """

    print(len(result), result)
    print(result_time)

