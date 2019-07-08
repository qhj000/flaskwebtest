from app import db, Post
from app.blog.models import Post

#
# # 测试数据库
# db.create_all()
# # print(app.config['SECRET_KEY'])
# # db.drop_all()
# # email = '112953821@qq.com'
# # user = User.query.filter_by(email=email).first()
# #
# # print(user)
#
# # print('abc'.encode())
#
# import sqlalchemy
# print(sqlalchemy.__version__)
#分页问题
posts = Post.query.paginate(page=2,per_page=2).items

lst = [post for post in posts]
print(lst)
