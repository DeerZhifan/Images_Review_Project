# -*- coding: utf-8 -*-
from sensitive_vocabulary import SensitiveVocabulary
from image_processing import ImageProcessing
import os
import re
import pytesseract


class RecognitionEngine():
    """敏感信息识别引擎"""
    def __init__(self, img_name, sub_imgs, sensitive_vocabulary):
        """初始化参数"""
        self.img_name = img_name
        self.sub_imgs = sub_imgs
        self.sensitive_vocabulary = sensitive_vocabulary

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
        character = self.get_character()
        for char in character:
            if char in self.sensitive_vocabulary:
                return "含敏感信息: {:}".format(char)
        return "不含敏感信息"


if __name__ == '__main__':
    imgs_path = '/users/vita/desktop/test4'
    vocabulary_path = '/users/vita/desktop/sensitive_vocabulary'
    vocabulary_engine = SensitiveVocabulary(vocabulary_path)
    sensitive_vocabulary = vocabulary_engine.build()
    imgs_name = os.listdir(imgs_path)
    result = {}
    if '.DS_Store' in imgs_name:
        imgs_name.remove('.DS_Store')
    for img_name in imgs_name:
        img_path = os.path.join(imgs_path, img_name)
        processing_engine = ImageProcessing(img_name, img_path)
        sub_imgs = processing_engine.get_tailored_img()
        recognition_engine = RecognitionEngine(img_name, sub_imgs, sensitive_vocabulary)
        result[img_name] = recognition_engine.recognizer()
    print(result)
