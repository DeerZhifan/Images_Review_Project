# -*- coding: utf-8 -*-
from database.setting import config

import pymysql
import requests
import pandas as pd


class ImageDownload:
    """下载图片"""
    def __init__(self, db_name, key=None, user=None, password=None, host=None, port=None):
        """初始化数据库连接信息"""
        self.db_name = db_name

        if key is None:
            self.key = "dev_algo_mysql"
        else:
            self.key = key

        if user is None:
            self.user = config[self.key]['user']
        else:
            self.user = user

        if password is None:
            self.password = config[self.key]['password']
        else:
            self.password = password

        if host is None:
            self.host = config[self.key]['host']
        else:
            self.host = host

        if port is None:
            self.port = config[self.key]['port']
        else:
            self.port = port

    def __get_imageurl(self):
        """从数据库中获取图片URL"""
        connect = pymysql.connect(db=self.db_name, user=self.user, password=self.password, host=self.host, port=self.port)
        sql = """
            SELECT imageId, imageURL 
            FROM algo_images_review_project
            WHERE reviewStatus=0;
            """
        rawdata = pd.read_sql(sql, connect)
        imageurls = {}
        for imageid in rawdata["imageId"]:
            imageurls[imageid] = rawdata["imageURL"][int(imageid)-1]
        return imageurls

    def __download_engine(self, imageid, imageurl):
        """下载引擎"""
        response = requests.get(imageurl)
        if response.status_code == 200:
            with open("./images/{:}.jpg".format(imageid), "wb") as f:
                f.write(response.content)
                f.close()

    def download(self):
        """下载图片"""
        imageurls = self.__get_imageurl()
        # print(imageurls)
        for imageid, imageurl in imageurls.items():
            self.__download_engine(imageid, imageurl)
        return None


if __name__ == "__main__":
    download_engine = ImageDownload(db_name="algorithm", key="dev_algo_mysql")
    download_engine.download()
