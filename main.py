# -*- coding: utf-8 -*-

from recognition_engine import RecognitionEngine
from classification_engine import ClassificationEngine
import os
import torch
from dataset import MyDataset
from torch.autograd import Variable
from torch.utils.data import DataLoader
from image_processing import ImageProcessing


class Main():
    """图片审核算法主程序"""
    def __init__(self, imgs_path, imgs_name, model_path, vocabulary_path):
        """初始化参数"""
        self.imgs_path = imgs_path
        self.imgs_name = imgs_name
        self.model_path = model_path
        self.vocabulary_path = vocabulary_path

    def review(self):
        """审核器"""
        datasets = MyDataset(self.imgs_path)
        dataloader = DataLoader(datasets, batch_size=1)
        classification_engine = ClassificationEngine(self.imgs_name, self.model_path)
        classified_result = classification_engine.classifier(dataloader)
        imgs_autopart = classified_result["配件"]
        recognized_result = {}
        for img_name in imgs_autopart:
            img_path = os.path.join(self.imgs_path, img_name)
            processing_engine = ImageProcessing(img_name, img_path)
            sub_imgs = processing_engine.get_tailored_img()
            recognition_engine = RecognitionEngine(img_name, sub_imgs, self.vocabulary_path)
            recognized_result[img_name] = recognition_engine.recognizer()
        return classified_result, recognized_result


if __name__ == '__main__':
    imgs_path = '/users/vita/desktop/test'
    imgs_name = os.listdir(imgs_path)
    model_path = 'resnet18.model'
    vocabulary_path = '/users/vita/desktop/sensitive_vocabulary'
    if '.DS_Store' in imgs_name:
        imgs_name.remove('.DS_Store')
    review_engine = Main(imgs_path, imgs_name, model_path, vocabulary_path)
    classified_result, recognized_result = review_engine.review()

