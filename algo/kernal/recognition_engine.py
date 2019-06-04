# -*- coding: utf-8 -*-
from algo.kernal.image_processing import ImageProcessing
from algo.common.setting import local_config
from algo.common.logger import log

import os
import re
import time
import pytesseract


class RecognitionEngine(object):
    """敏感信息识别引擎"""
    def __init__(self, image_name, sub_images, vocabulary_path):
        """初始化参数"""
        self.image_name = image_name
        self.sub_images = sub_images
        self.vocabulary_path = vocabulary_path
        
    def build_vocabulary(self):
        """建立敏感信息库"""
        log.info("加载敏感信息库......")
        vocabulary = []
        with open(self.vocabulary_path, 'r', encoding="UTF-8") as f:
            while True:
                line = f.readline().split('\n')[0]
                if not line:
                    break
                else:
                    vocabulary.append(line)
        log.info("加载成功！")
        return vocabulary
    
    def get_character(self,):
        """识别字符"""
        log.info("开始从图片中识别字符......")
        character = []
        for sub_image in self.sub_images[self.image_name]:
            text = pytesseract.image_to_string(sub_image, lang='chi_sim', config='--psm 6')
            re_text = re.sub('[^\u4e00-\u9fa5a-zA-Z]+', ' ', text).replace('_', ' ')    # 过滤非中英文字符
            if len(re_text) >= 2:
                clean_text = re_text.lower().strip().split(' ')
                character.extend(clean_text)
        log.info("识别完毕！")
        return character

    def recognizer(self):
        """识别器"""
        sensitive_vocabulary = self.build_vocabulary()
        character = self.get_character()
        log.info("识别出字符：{}".format(character))
        for char in character:
            if char in sensitive_vocabulary:
                return 0
        for char in character:
            if char in ''.join(sensitive_vocabulary) and len(char) > 1:
                return 0
        return 1


if __name__ == '__main__':
    parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    image_path = os.path.join(parent_path, local_config["image_path"])
    vocabulary_path = os.path.join(parent_path, local_config["vocabulary_path"])
    image_name = os.listdir(image_path)
    result = {}
    result_time = {}
    if '.DS_Store' in image_name:
        image_name.remove('.DS_Store')
    for img_name in image_name:
        since = time.time()
        img_path = os.path.join(image_path, img_name)
        processing_engine = ImageProcessing(img_name, img_path)
        sub_images = processing_engine.get_tailored_img()
        recognition_engine = RecognitionEngine(img_name, sub_images, vocabulary_path)
        sensitive_flag = recognition_engine.recognizer()
        result[img_name] = sensitive_flag
        result_time[img_name] = time.time() - since
    print(len(result), result)
    print(result_time)

