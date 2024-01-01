# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy()

# 定义一个书签模型，继承自 SQLAlchemy 基类，对应于数据库中的 bookmarks 表
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=False)
    box_shadow = Column(String(255), nullable=False)

    def __repr__(self):
        return '<Bookmark %r>' % self.name

# 定义一个书签2模型，继承自 SQLAlchemy 的基类
class Bookmark2(Base):
    # 指定表名为 bookmarks2
    __tablename__ = 'bookmarks2'
    # 定义表中的字段，包括类型和主键
    category = Column(String(50), primary_key=True)
    name = Column(String(100), primary_key=True)
    link = Column(String(255))
    description = Column(String(255))