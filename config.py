import os


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    # 设置密匙要没有规律，别被人轻易猜到哦
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mysql:123456@192.168.80.130:3306/school?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
