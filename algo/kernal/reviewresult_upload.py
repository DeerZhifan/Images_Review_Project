# -*- coding: utf-8 -*-

from algo.kernal.db_setup import MySql
from algo.common.logger import log

import datetime
from sqlalchemy import Table


class ReviewResultUpload(object):
    """上传图片审核结果"""
    def __init__(self, image_url, review_result):
        """初始化数据库连接信息"""
        self.image_url = image_url
        self.review_result = review_result

    def url_check(self):
        """检查image_url是否已在数据库中"""
        engine = MySql(key='algo_mysql')
        session = engine.get_session()
        model = engine.get_model()
        images_review_model = model.classes.algo_images_review_result
        image_url_query = session.query(images_review_model.image_url).filter(images_review_model.image_url == self.image_url)
        image_url = []
        for data in image_url_query:
            image_url.append(data.image_url)
        if self.image_url in image_url:
            return False
        else:
            return True

    def upload(self):
        """上传结果"""
        engine = MySql(key='algo_mysql')
        metadata = engine.get_metadata()
        session = engine.get_session()
        connect = engine.get_connection()
        flag = self.url_check()
        if flag:
            algo_images_review_result = Table("algo_images_review_result", metadata, autoload=True)
            result_dict = dict()
            result_dict["image_url"] = self.image_url
            result_dict["review_result"] = self.review_result
            result_dict["update_time"] = datetime.datetime.now()
            connect.execute(algo_images_review_result.insert(), result_dict)
        else:
            log.info("该图片已被审核！")
        session.close()
        return None


if __name__ == "__main__":
    image_url = "http://test-pic.qipeipu.net/erp/10000/erpResource/pic/partsImage/25ab0d60-b6b6-4528-94ff-709272739794.jpg"
    review_result = 1
    engine = ReviewResultUpload(image_url, review_result)
    engine.upload()
