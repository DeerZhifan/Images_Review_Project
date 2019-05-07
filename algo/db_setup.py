# -*- coding: utf-8 -*-
from algo.setting import pyconfig

from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TINYINT
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import Table
import warnings
warnings.filterwarnings('ignore')


class MySql(object):
    """连接数据库"""
    def __init__(self, key=None, database=None, user=None, password=None, host=None, port=None):
        """初始化数据库连接信息"""
        db_url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"

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

        self.db_url = db_url.format(user=self.user, password=self.password, host=self.host, port=self.port,
                                    database=self.database)

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
    def __init__(self, key=None, database=None, user=None, password=None, host=None, port=None):
        """初始化"""
        super(CreateTable, self).__init__(key=key, database=database, user=user, password=password, host=host, port=port)
        self.metadata = self.get_metadata()

    def algo_images_review_project(self):
        """图片审核表设计"""
        algo_images_review_project = Table("algo_images_review_project", self.metadata,
                                           Column("image_id", INTEGER, primary_key=True, autoincrement=True, comment="图片ID"),
                                           Column("image_url", VARCHAR(200), nullable=False, comment="图片URL"),
                                           Column("review_status", TINYINT(1), nullable=False, server_default="0", comment="图片审核状态：0未审核，1已审核"),
                                           Column("review_result", TINYINT(1), nullable=False, server_default="0", comment="图片审核结果：0不合规，1合规"),
                                           Column("create_time", DateTime, server_default=func.now(), comment="创建时间"),
                                           Column("update_time", DateTime, server_default=func.now(), server_onupdate=func.now(), comment="更新时间"),
                                           Column("is_deleted", TINYINT(1), nullable=False, server_default="0", comment="删除标识: 0未删除，1删除"))
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
    engine = CreateTable(key="algo_mysql")
    engine.create_table()
    # engine.drop_table()

    # 测试插入数据

    engine = MySql(key='algo_mysql')
    model = engine.get_model()
    metadata = engine.get_metadata()
    session = engine.get_session()
    connect = engine.get_connection()
    test_list = []
    imageurls = ["https://pic.qipeipu.com/uploadpic/16864/6bbbc5305a481857646efff9d4f9b6d7.jpg",
                 "https://pic.qipeipu.com/uploadpic/210576/3957d7fcf9aeca766907bcad146d2d60.jpg",
                 "https://pic.qipeipu.com/uploadpic/16861/4a5b06ddabf2c9006bb1ba21f5ade696.jpg",
                 "https://pic.qipeipu.com/uploadpic/210576/8ca4221d591853da687e925c78c54fef.jpg",
                 "https://pic.qipeipu.com/uploadpic/210576/64fef0b2e9345b37b8a70af97f769f0c.jpg",]
    for imageurl in imageurls:
        test_dict = {}
        test_dict["image_url"] = imageurl
        test_list.append(test_dict)
    algo_images_review_project = Table("algo_images_review_project", metadata, autoload=True)
    connect.execute(algo_images_review_project.insert(), test_list)
    session.close()
