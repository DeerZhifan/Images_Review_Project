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
                status_code = response.status_code
                content_length = response.headers["Content-Length"]
                if status_code == 200 and content_length != "0":
                    log.info("下载成功！")
                    log.info("保存图片......")
                    with open("{:}/{:}.jpg".format(image_path, image_name), "wb") as f:
                        f.write(response.content)
                        f.close()
                        log.info("保存成功！")
                        return True
            except:
                run_cnt += 1
                self.__download_engine(image_path, image_name, image_url, run_cnt)
        log.info("图片无法下载！")
        return False

    def download(self):
        """下载图片"""
        parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        image_path = os.path.join(parent_path, local_config["image_path"])
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_name = self.image_url[-9:-4]
        log.info("图片信息，image_url:{}".format(self.image_url))
        log.info("下载中......")
        flag = self.__download_engine(image_path, image_name, self.image_url)
        return flag


if __name__ == "__main__":
    image_url = "http://test-pic.qipeipu.net/erp/10000/erpResource/pic/partsImage/25ab0d60-b6b6-4528-94ff-709272739794.jpg"
    download_engine = ImageDownload(image_url=image_url)
    result = download_engine.download()
    print(result)

