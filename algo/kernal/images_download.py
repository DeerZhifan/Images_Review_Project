# -*- coding: utf-8 -*-
from algo.common.setting import local_config
from algo.common.logger import log

import os
import requests


class ImageDownload(object):
    """下载图片"""
    def __init__(self, image_url):
        """初始化下载信息"""
        self.image_url = image_url

    def __download_engine(self, image_path, image_name, image_url, run_cnt=0):
        """下载引擎"""
        if run_cnt <= 3:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    log.info("下载成功！")
                    log.info("保存图片......")
                    with open("{:}/{:}.jpg".format(image_path, image_name), "wb") as f:
                        f.write(response.content)
                        f.close()
                        log.info("保存成功！")
            except:
                run_cnt += 1
                self.__download_engine(image_path, image_name, image_url, run_cnt)
        return None

    def download(self):
        """下载图片"""
        parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        image_path = os.path.join(parent_path, local_config["image_path"])
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_name = self.image_url[-9:-4]
        log.info("图片信息，image_url:{}".format(self.image_url))
        log.info("下载中......")
        self.__download_engine(image_path, image_name, self.image_url)
        return None


if __name__ == "__main__":
    image_url = "https://pic.qipeipu.com/uploadpic/234775/58cd2d6b76a06305813b76d1edc3fa86.jpg"
    download_engine = ImageDownload(image_url=image_url)
    download_engine.download()

