# -*- coding: utf-8 -*-
from algo.setting import pyconfig
from algo.setting import local_config

import os
import pymysql
import requests
import pandas as pd


class ImageDownload(object):
    """下载图片"""
    def __init__(self, key=None, database=None, user=None, password=None, host=None, port=None):
        """初始化数据库连接信息"""
        parent_path = os.path.dirname(os.path.dirname(__file__))
        self.imgs_path = os.path.join(parent_path, local_config["images_path"])

        if key is None:
            self.key = "algo_mysql"
        else:
            self.key = key

        if database is None:
            self.database = pyconfig[self.key]['database']
        else:
            self.database = database

        if user is None:
            self.user = pyconfig[self.key]['user']
        else:
            self.user = user

        if password is None:
            self.password = pyconfig[self.key]['password']
        else:
            self.password = password

        if host is None:
            self.host = pyconfig[self.key]['host']
        else:
            self.host = host

        if port is None:
            self.port = pyconfig[self.key]['port']
        else:
            self.port = port

    def __get_imageurl(self):
        """从数据库中获取图片URL"""
        connect = pymysql.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        sql = """
            SELECT image_id, image_url 
            FROM algo_images_review_project
            WHERE review_status=0;
            """
        rawdata = pd.read_sql(sql, connect)
        imageurls = {}
        index = 0
        for imageid in rawdata["image_id"]:
            imageurls[imageid] = rawdata["image_url"][index]
            index += 1
        return imageurls

    def __download_engine(self, imageid, imageurl):
        """下载引擎"""
        response = requests.get(imageurl)
        if response.status_code == 200:
            with open("{:}/{:}.jpg".format(self.imgs_path, imageid), "wb") as f:
                f.write(response.content)
                f.close()

    def download(self):
        """下载图片"""
        imageurls = self.__get_imageurl()
        if not os.path.exists(self.imgs_path):
            os.makedirs(self.imgs_path)
        for imageid, imageurl in imageurls.items():
            self.__download_engine(imageid, imageurl)
        return None


if __name__ == "__main__":
    download_engine = ImageDownload(key="algo_mysql")
    download_engine.download()
