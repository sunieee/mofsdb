from typing import overload
from xml.etree.ElementTree import Comment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import func
db = SQLAlchemy()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:digitalmofs@actvis.cn:9049/mofsdb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
db.session = DBSession()

class BaseModel(db.Model):
    __abstract__ = True

    def add(self):
        """
        新增数据
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        更新数据
        :return:
        """
        db.session.merge(self)
        db.session.commit()

    def delete(self):
        """
        删除数据
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def add_all(self, data):
        db.session.excute(
            self.__table__.insert(),
            data
        )
        db.session.commit()
        
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

