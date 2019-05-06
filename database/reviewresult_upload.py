# -*- coding: utf-8 -*-

from database.db_setup import MySql
import datetime
from sqlalchemy import Table


class ReviewResultUpload:
    """上传图片审核结果"""
    def __init__(self, reviewresult):
        """初始化数据库连接信息"""
        self.reviewresult = reviewresult

    def upload(self):
        """上传结果"""
        engine = MySql(db_name='algorithm', key='dev_algo_mysql')
        metadata = engine.get_metadata()
        session = engine.get_session()
        connect = engine.get_connection()
        algo_images_review_project = Table("algo_images_review_project", metadata, autoload=True)
        for imageid, result in self.reviewresult.items():
            result_dict = dict()
            result_dict["review_status"] = 1
            result_dict["review_result"] = result
            result_dict["update_time"] = datetime.datetime.now()
            connect.execute(algo_images_review_project.update().\
                        where(algo_images_review_project.c.image_id == imageid).\
                        values(result_dict))

        session.close()
        return None


if __name__ == "__main__":
    reviewresult = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 1}
    engine = ReviewResultUpload(reviewresult)
    engine.upload()
