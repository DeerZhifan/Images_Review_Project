# -*- coding: utf-8 -*-

from algo.kernal.db_setup import MySql

import datetime
from sqlalchemy import Table


class ReviewResultUpload(object):
    """上传图片审核结果"""
    def __init__(self, image_url, review_result):
        """初始化数据库连接信息"""
        self.image_url = image_url
        self.review_result = review_result

    def upload(self):
        """上传结果"""
        engine = MySql(key='algo_mysql')
        metadata = engine.get_metadata()
        session = engine.get_session()
        connect = engine.get_connection()
        algo_images_review_project = Table("algo_images_review_result", metadata, autoload=True)
        for _, result in self.review_result.items():
            result_dict = dict()
            result_dict["image_url"] = self.image_url
            result_dict["review_result"] = result
            result_dict["update_time"] = datetime.datetime.now()
            connect.execute(algo_images_review_project.insert(), result_dict)

        session.close()
        return None


if __name__ == "__main__":
    image_url = "https://pic.qipeipu.com/uploadpic/16864/6bbbc5305a481857646efff9d4f9b6d7.jpg"
    review_result = {'9b6d7.jpg': 1}
    engine = ReviewResultUpload(image_url, review_result)
    engine.upload()
