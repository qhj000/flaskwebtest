from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from app.blog.models import User, Post, Content
from app import app, db
from flask import render_template, flash, url_for, request, jsonify
from app.blog.forms import LoginForm
import bcrypt
import datetime
from app.blog.services import gen_token, authenticate


@app.route('/blog')
@app.route('/blog/index')
def index():
    """
    简单的首页测试
    :return:
    """
    user = {'username': 'duke'}
    posts = [
        {
            'author': {'username': '哈哈'},
            'body': '这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '呵呵'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html', title='我的', user=user, posts=posts)


@app.route('/blog/login', methods=['GET', 'POST'])
def login():
    """

    测试

    :return:
    """
    form = LoginForm()
    # 验证表格中的数据格式是否正确
    if form.validate_on_submit():
        # 闪现的信息会出现在页面，当然在页面上要设置
        flash('用户登录的名户名是:{} , 是否记住我:{}'.format(
            form.username.data, form.remember_me.data))
        # 重定向至首页
        return redirect(url_for('index'))
    # 首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title='登录', form=form)


@app.route('/blog/test', methods=['GET', 'POST'])
def test():
    method = request.method
    get_value = request.args  # GET请求的值
    post_value = request.values
    return 'method:{},get_value:{},post_value:{}'.format(method, get_value, post_value)


@app.route('/blog/user/reg', methods=['POST'])
def reg():
    """
    用于注册blog用户
    :return: token
    """
    # payload = json.loads(request.data.decode())
    payload = request.json
    try:

        email = payload['email']
        # user = db.query(User).filter.
        query = User.query.filter_by(email=email).first()

        if query:
            return abort(400)
        name = payload['name']
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
        print(email, name, password)
        user = User()
        user.email = email
        user.name = name
        user.password = password
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify({'token': gen_token(user.id)})  # 如果正常，返回json数据
        except Exception as e:
            print(e)
            raise
    except Exception as e:
        print(e)
        return abort(400)


@app.route('/blog/user/login', methods=['POST'])
def login2():
    """
    用户blog用户的登陆
    :return: user and token
    """
    # payload = json.loads(request.data.decode())  # json转换成字典
    payload = request.json
    print(payload)
    try:
        email = payload['email']
        user = User.query.filter_by(email=email).first()

        if bcrypt.checkpw(payload['password'].encode(), user.password.encode()):
            # 验证通过
            token = gen_token(user.id)
            # print(token)
            res = {
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email
                }, 'token': token
            }
            # 这里还可以setcookie
            return jsonify(res)
        else:
            return abort(400)

    except Exception as e:  # 有任何异常，都返回
        print(e)
        return abort(400)  # 这里返回实例，这不是异常类


@app.route('/blog/hello', methods=['GET', 'POST'])
@authenticate
def hello():
    """
    :return: 测试认证装饰器,认证一定要在路由下面
    """
    print(request.user)  # 获取装饰器注入的user
    return 'hello'


@app.route('/blog/pub', methods=['POST'])
@authenticate
def pub():
    """
    用户从浏览器端提交Json数据，包含title，content。 提交博文需要认证用户，从请求的header中验证jw
    :return:
    """
    post = Post()
    content = Content()
    try:
        payload = request.json
        post.title = payload['title']
        post.author = request.user.id
        post.postdate = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8))
        )
        db.session.add(post)
        db.session.commit()
        content.content = payload['content']
        content.post_id = post.id
        db.session.add(content)
        db.session.commit()
        return jsonify({'post_id': post.id})

    except Exception as e:
        print(e)
        return abort(400)


@app.route('/blog/pub1', methods=['POST'])
@authenticate
def pub1():
    return 'hello'


@app.route('/blog/post/<string:ids>', methods=['GET'])
def get(ids):
    try:
        id = int(ids)
        post = Post.query.filter_by(id=id).first()

        print(post.content.content, '~~~~')

        if post:
            return jsonify({
                'post': {
                    'post_id': post.id,
                    'title': post.title,
                    'author_id': post.author,
                    'author': post.user.name,
                    'postdate': post.postdate,
                    'content': post.content.content
                }
            })
    except Exception as e:
        print(e)
        return abort(404)

