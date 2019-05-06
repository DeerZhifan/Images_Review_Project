# -*- coding: utf-8 -*-

from database.images_download import ImageDownload
from database.reviewresult_upload import ReviewResultUpload
from recognition.image_processing import ImageProcessing
from recognition.recognition_engine import RecognitionEngine
from classification.dataset import MyDataset
from classification.classification_engine import ClassificationEngine
import os
from torch.utils.data import DataLoader


class Main:
    """图片审核算法主程序"""
    def __init__(self, db_name, key, imgs_path, model_path, vocabulary_path):
        """初始化参数"""
        self.db_name = db_name
        self.key = key
        self.imgs_path = imgs_path
        self.model_path = model_path
        self.vocabulary_path = vocabulary_path
        self.image_download()
        self.imgs_name = os.listdir(imgs_path)

    def image_download(self):
        """下载图片"""
        download_engine = ImageDownload(self.db_name, self.key)
        download_engine.download()

    def result_upload(self, review_result):
        """将审核结果上传至数据库"""
        upload_engine = ReviewResultUpload(review_result)
        upload_engine.upload()

    def images_delete(self):
        """审核结束后删除images"""
        for img_name in self.imgs_name:
            os.remove(os.path.join(self.imgs_path, img_name))

    def review(self):
        """审核器"""
        datasets = MyDataset(self.imgs_path)
        dataloader = DataLoader(datasets, batch_size=1)
        classification_engine = ClassificationEngine(self.imgs_name, self.model_path)
        classified_result = classification_engine.classifier(dataloader)
        review_result = {}
        for img_name, result in classified_result.items():
            imageid = img_name.split(".")[0]
            if result == 0:
                review_result[imageid] = result
            else:
                img_path = os.path.join(self.imgs_path, img_name)
                processing_engine = ImageProcessing(img_name, img_path)
                sub_imgs = processing_engine.get_tailored_img()
                recognition_engine = RecognitionEngine(img_name, sub_imgs, self.vocabulary_path)
                review_result[imageid] = recognition_engine.recognizer()
        self.result_upload(review_result)
        self.images_delete()


if __name__ == '__main__':
    db_name = "algorithm"
    key = "dev_algo_mysql"
    imgs_path = "C:\\Users\\ABC\\PycharmProjects\\Images_Review_Project\\images"
    model_path = "C:\\Users\\ABC\\PycharmProjects\\Images_Review_Project\\classification\\resnet18.model"
    vocabulary_path = "C:\\Users\\ABC\\PycharmProjects\\Images_Review_Project\\recognition\\sensitive_vocabulary.txt"
    review_engine = Main(db_name, key, imgs_path, model_path, vocabulary_path)
    review_engine.review()




