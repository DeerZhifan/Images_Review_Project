# -*- coding: utf-8 -*-
from database.setting import config

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, TIMESTAMP, Boolean
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import Table
import datetime
import warnings
warnings.filterwarnings('ignore')


class MySql(object):
    """连接数据库"""
    def __init__(self, db_name, key=None, user=None, password=None, host=None, port=None):
        """初始化数据库连接信息"""
        db_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"

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

        self.db_url = db_url.format(user=self.user, password=self.password, host=self.host, port=self.port,
                                    db_name=self.db_name)

    def get_engine(self):
        """建立数据库连接"""
        engine = create_engine(self.db_url, encoding="utf-8")
        return engine

    def get_metadata(self):
        """建立metadata对象，绑定数据库引擎"""
        engine = self.get_engine()
        metadata = MetaData(engine)
        return metadata

    def get_connection(self):
        """建立连接"""
        engine = self.get_engine()
        connection = engine.connect()
        return connection

    def get_session(self):
        """建立会话"""
        session_class = sessionmaker()
        engine = self.get_engine()
        session_class.configure(bind=engine)
        session = session_class()
        return session

    def get_model(self):
        """映射指定的表"""
        engine = self.get_engine()
        reflect_meta = MetaData()
        reflect_meta.reflect(engine)
        db_model = automap_base(metadata=reflect_meta)
        db_model.prepare()
        return db_model


class CreateTable(MySql):
    """建立记录图片审核状态的数据表"""
    def __init__(self, db_name, key=None, user=None, password=None, host=None, port=None):
        """初始化"""
        super(CreateTable, self).__init__(db_name=db_name, key=key, user=user, password=password, host=host, port=port)
        self.metadata = self.get_metadata()

    def algo_images_review_project(self):
        """图片审核表设计"""
        algo_images_review_project = Table("algo_images_review_project", self.metadata,
                                           Column("imageId", Integer, primary_key=True, autoincrement=True, comment="图片ID"),
                                           Column("imageURL", String(100), nullable=False, comment="图片URL"),
                                           Column("reviewStatus", Boolean, nullable=False, comment="图片审核状态：0未审核，1已审核"),
                                           Column("reviewResult", Boolean, nullable=False, comment="图片审核结果：0不合规，1合规"),
                                           Column("createTime", TIMESTAMP, nullable=False, comment="创建时间"),
                                           Column("updateTime", TIMESTAMP, nullable=False, comment="创建时间"),
                                           Column("isDeleted", Boolean, nullable=False, comment="删除标识: 0未删除，1删除"))
        return algo_images_review_project

    def create_table(self):
        """创建表"""
        self.algo_images_review_project()
        self.metadata.create_all()
        return None

    def drop_table(self):
        """删除表"""
        self.algo_images_review_project()
        self.metadata.drop_all()
        return None


if __name__ == "__main__":
    # 建表
    engine = CreateTable(db_name="algorithm", key="dev_algo_mysql")
    engine.create_table()
    # engine.drop_table()

    # 测试插入数据
    """
    engine = MySql(db_name='algorithm', key='dev_algo_mysql')
    model = engine.get_model()
    metadata = engine.get_metadata()
    session = engine.get_session()
    connect = engine.get_connection()
    test_list = []
    test_dict = {}
    test_dict["imageId"] = 0
    test_dict["imageURL"] = "www.facebook.com"
    test_dict["reviewStatus"] = 0
    test_dict["reviewResult"] = 0
    test_dict["createTime"] = datetime.datetime.now()
    test_dict["updateTime"] = datetime.datetime.now()
    test_dict["isDeleted"] = 0
    test_list.append(test_dict)
    algo_images_review_project = Table("algo_images_review_project", metadata, autoload=True)
    connect.execute(algo_images_review_project.insert(), test_list)
    session.close()
    """