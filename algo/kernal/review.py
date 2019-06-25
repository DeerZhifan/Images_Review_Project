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


class ImagesReview(object):
    """图片审核算法主程序"""
    def __init__(self, key, image_url):
        """初始化参数"""
        log.info("图片审核算法开始运行......")
        log.info(">>>>>>>>>>>>>>>>>>>>初始化<<<<<<<<<<<<<<<<<<<<")
        log.info("初始化图片路径、分类模型路径及敏感词汇库路径......")
        self.key = key
        self.image_url = image_url
        parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.image_path = os.path.join(parent_path, local_config["image_path"])
        self.model_path = os.path.join(parent_path, local_config["model_path"])
        self.vocabulary_path = os.path.join(parent_path, local_config["vocabulary_path"])
        log.info("初始化完毕！")
        self.flag = self.image_download()
        self.image_name = self.image_url[-9:]

    def image_download(self):
        """下载图片"""
        log.info(">>>>>>>>>>>>>>>>>>>图片下载<<<<<<<<<<<<<<<<<<<")
        log.info("启动图片下载引擎......")
        download_engine = ImageDownload(self.image_url)
        flag = download_engine.download()
        if flag:
            log.info("下载程序执行完毕！")
        else:
            log.info("下载结束！")
        return flag

    def result_upload(self, review_result):
        """将审核结果上传至数据库"""
        log.info("将审核结果上传至数据库中......")
        upload_engine = ReviewResultUpload(self.image_url, review_result)
        upload_engine.upload()
        log.info("上传完毕！")

    def images_delete(self):
        """审核结束后删除图片"""
        log.info("删除已审核图片......")
        os.remove(os.path.join(self.image_path, self.image_name))
        log.info("删除完毕！")

    def review(self):
        """审核器"""
        log.info(">>>>>>>>>>>>>>>>>>>图片审核<<<<<<<<<<<<<<<<<<<")
        review_result = 0
        if self.flag:
            log.info(">>>>>>>>>>>>>>>>步骤1：图片分类<<<<<<<<<<<<<<<<")
            datasets = MyDataset(self.image_path, self.image_name)
            dataloader = DataLoader(datasets, batch_size=1)
            classification_engine = ClassificationEngine(self.image_name, self.model_path)
            classified_result = classification_engine.classifier(dataloader)
            log.info(">>>>>>>>>>>>>>步骤2：敏感信息识别<<<<<<<<<<<<<<")
            for img_name, result in classified_result.items():
                if result == 0:
                    review_result = result
                else:
                    img_path = os.path.join(self.image_path, img_name)
                    processing_engine = ImageProcessing(img_name, img_path)
                    sub_images = processing_engine.get_tailored_img()
                    recognition_engine = RecognitionEngine(img_name, sub_images, self.vocabulary_path)
                    review_result = recognition_engine.recognizer()
            log.info(">>>>>>>>>>>>>>>>>>>审核结束<<<<<<<<<<<<<<<<<<<")
            self.images_delete()
        self.result_upload(review_result)
        log.info("图片审核算法执行完毕！")
        return review_result


if __name__ == '__main__':
    image_url = "https://pic.qipeipu.com/uploadpic/16864/98571da8c295bd138e992d4a6623369a.jpg"
    review_engine = ImagesReview(key="algo_mysql", image_url=image_url)
    result = review_engine.review()
    print(result)






