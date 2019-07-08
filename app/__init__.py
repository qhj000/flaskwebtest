from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
"""
初始化app，进行配置，导入路由
"""
app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from app.blog.models import * #数据模型类
from app.blog import controllers