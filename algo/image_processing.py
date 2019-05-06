# -*- coding: utf-8 -*-

import cv2
import pytesseract


class ImageProcessing():
    """图片预处理"""
    def __init__(self, img_name, img_path):
        """初始化"""
        self.img_name = img_name
        self.img_path = img_path

    def get_image(self, flag):
        """读取图片"""
        if flag == 'COLOR':
            img = cv2.imread(self.img_path, cv2.IMREAD_COLOR)
            if img.shape[0] > 1000 and img.shape[1] > 1000:
                img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
        elif flag == 'GRAYSCALE':
            img = cv2.imread(self.img_path, cv2.IMREAD_GRAYSCALE)
            if img.shape[0] > 1000 and img.shape[1] > 1000:
                img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
        else:
            print('Please choose the right flag: COLOR OR GRAYSCALE.')
            return None
        return img

    def get_binary_image(self):
        """获取二值化图片"""
        flag = 'GRAYSCALE'
        img = self.get_image(flag)
        _, binary_img = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
        return binary_img

    def get_medianblur_img(self):
        """获取中值滤波图片"""
        binary_img = self.get_binary_image()
        medianblur_img = cv2.medianBlur(binary_img, 5)
        return medianblur_img

    def get_opened_image(self):
        """获取开运算图片"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        medianblur_img = self.get_medianblur_img()
        opened_img = cv2.morphologyEx(medianblur_img, cv2.MORPH_OPEN, kernel)
        return opened_img

    def get_closed_image(self):
        """"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        medianblur_img = self.get_medianblur_img()
        closed_img = cv2.morphologyEx(medianblur_img, cv2.MORPH_CLOSE, kernel)
        return closed_img

    def get_inversed_img(self, switch_status):
        """黑白反色"""
        if switch_status == 'open':
            opened_img = self.get_opened_image()
            inversed_img = cv2.bitwise_not(opened_img)
        elif switch_status == 'close':
            closed_img = self.get_closed_image()
            inversed_img = cv2.bitwise_not(closed_img)
        else:
            print('Please choose the right switch status: open OR close.')
            return None
        return inversed_img

    def get_contours(self, switch_status):
        """获取轮廓"""
        inversed_img = self.get_inversed_img(switch_status)
        contours, _ = cv2.findContours(inversed_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def get_tailored_img(self):
        """裁剪出可能包含字符的区域"""
        sub_imgs = {}
        sub_imgs[self.img_name] = []
        binaryed_img = self.get_binary_image()
        for switch_status in ['open']:
            contours = self.get_contours(switch_status)
            useful_contours = []
            for i in contours:
                if len(i) in range(20, 500):
                    useful_contours.append(i)
            for contour in useful_contours:
                p_x, p_y = [], []
                for p in contour:
                    p_x.append(p[0][1])
                    p_y.append(p[0][0])
                x, y, x_, y_ = min(p_x), min(p_y), max(p_x), max(p_y)
                sub_imgs[self.img_name].append(binaryed_img[x:x_, y:y_])
        return sub_imgs


if __name__ == '__main__':
    img_name = '中网20.jpg'
    img_path = '/users/vita/desktop/中网20.jpg'
    engine = ImageProcessing(img_name, img_path)
    sub_imgs = engine.get_tailored_img()
    for img in sub_imgs[img_name]:
        print(type(img))
        text = pytesseract.image_to_string(img, lang='chi_sim', config='-psm 6')
        print(text)
