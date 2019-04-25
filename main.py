# -*- coding: utf-8 -*-

from recognition.recognition_engine import RecognitionEngine
from classification.classification_engine import ClassificationEngine
import os
import time
from classification.dataset import MyDataset
from torch.utils.data import DataLoader
from recognition.image_processing import ImageProcessing


class Main:
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
        recognized_result = {}
        for img_name, review_result in classified_result.items():
            imageid = img_name.split(".")[0]
            if review_result == 0:
                recognized_result[imageid] = review_result
            else:
                img_path = os.path.join(self.imgs_path, img_name)
                processing_engine = ImageProcessing(img_name, img_path)
                sub_imgs = processing_engine.get_tailored_img()
                recognition_engine = RecognitionEngine(img_name, sub_imgs, self.vocabulary_path)
                sensitive_information = recognition_engine.recognizer()
                recognized_result[imageid] = sensitive_information
        return recognized_result


if __name__ == '__main__':
    since = time.time()
    imgs_path = './images'
    imgs_name = os.listdir(imgs_path)
    model_path = './classification/resnet18.model'
    vocabulary_path = './recognition/sensitive_vocabulary.txt'
    if '.DS_Store' in imgs_name:
        imgs_name.remove('.DS_Store')
    review_engine = Main(imgs_path, imgs_name, model_path, vocabulary_path)
    recognized_result = review_engine.review()
    time_elapsed = time.time() - since
    m, s = divmod(time_elapsed, 60)
    h, m = divmod(m, 60)
    print('\nReview {:} images with {:.0f}h {:.0f}m {:.0f}s'.format(len(imgs_name), h, m, s))
    print(recognized_result)

