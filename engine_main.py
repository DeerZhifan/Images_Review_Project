# -*- coding: utf-8 -*-

from algo.common.setting import local_config
from algo.kernal.images_download import ImageDownload
from algo.kernal.reviewresult_upload import ReviewResultUpload
from algo.kernal.image_processing import ImageProcessing
from algo.kernal.recognition_engine import RecognitionEngine
from algo.kernal.dataset import MyDataset
from algo.kernal.classification_engine import ClassificationEngine
from algo.common.logger import log
import os
from torch.utils.data import DataLoader


class Main(object):
    """图片审核算法主程序"""
    def __init__(self, key):
        """初始化参数"""
        log.info("图片审核算法开始运行......")
        log.info("初始化图片路径、分类模型路径及敏感词汇库路径......")
        self.key = key
        current_path = os.path.dirname(__file__)
        self.imgs_path = os.path.join(current_path, local_config["images_path"])
        self.model_path = os.path.join(current_path, local_config["model_path"])
        self.vocabulary_path = os.path.join(current_path, local_config["vocalbulary_path"])
        log.info("初始化完毕！")
        self.image_download()
        self.imgs_name = os.listdir(self.imgs_path)

    def image_download(self):
        """下载图片"""
        log.info("从数据库中下载待审核图片......")
        download_engine = ImageDownload(self.key)
        download_engine.download()
        log.info("下载完毕！")

    def result_upload(self, review_result):
        """将审核结果上传至数据库"""
        log.info("将审核结果上传至数据库中......")
        upload_engine = ReviewResultUpload(review_result)
        upload_engine.upload()
        log.info("上传完毕！")

    def images_delete(self):
        """审核结束后删除images"""
        log.info("删除已审核图片......")
        for img_name in self.imgs_name:
            os.remove(os.path.join(self.imgs_path, img_name))
        log.info("删除完毕！")

    def review(self):
        """审核器"""
        log.info("审核开始......")
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
        log.info("审核结束！")
        self.result_upload(review_result)
        self.images_delete()
        log.info("图片审核算法执行完毕！")


if __name__ == '__main__':
    review_engine = Main(key="algo_mysql")
    review_engine.review()






