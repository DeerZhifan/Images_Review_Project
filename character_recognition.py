# -*- coding: utf-8 -*-
from sensitive_words_library import SensitiveWordsLibrary
from image_processing import ImageProcessing
import os
import re
import pytesseract


class CharacterRecognition():
    """提取出图片中的字符并进行敏感信息判别"""
    def __init__(self, img_name, textimg, sensitive_words):
        """初始化参数"""
        self.img_name = img_name
        self.textimg = textimg
        self.sensitive_words = sensitive_words
        self.sensitive_words_string = ''.join(self.sensitive_words)

    def get_character(self,):
        """提取字符"""
        character = []
        for img in self.textimg[self.img_name]:
            text = pytesseract.image_to_string(img, lang='chi_sim', config='-psm 6')
            re_text = re.sub('[^\w\u4e00-\u9fa5a-zA-Z]+', ' ', text).replace('_', ' ')    # 过滤非中英文字符
            if len(re_text) >= 2:
                clean_text = re_text.lower().strip().split(' ')
                character.extend(clean_text)
        return character

    def issensitive(self):
        """敏感信息判别"""
        character = self.get_character()
        for word in character:
            if word in self.sensitive_words:
                print('{:} contains sensitive information: "{:}".'.format(self.img_name, word))
                return True
        print('{:} is clean.'.format(self.img_name))
        return False


if __name__ == '__main__':
    sensitive_imgs = 0
    img_root = '/users/vita/desktop/test'
    words_root = '/users/vita/desktop/sensitive_words'
    sensitive_engine = SensitiveWordsLibrary(words_root)
    sensitive_words = sensitive_engine.build()
    img_names = os.listdir(img_root)
    for img_name in img_names:
        img_path = os.path.join(img_root, img_name)
        processing_engine = ImageProcessing(img_name, img_path)
        textimg = processing_engine.get_tailored_img()
        recognition_engine = CharacterRecognition(img_name, textimg, sensitive_words)
        result = recognition_engine.issensitive()
        if result:
            sensitive_imgs += 1
    print("There are {:} images that contained sensitive information.".format(sensitive_imgs))