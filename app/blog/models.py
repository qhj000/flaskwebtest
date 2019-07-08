from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(48), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<user {} {}>'.format(self.id, self.name)

    __str__ = __repr__


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    postdate = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    user = db.relationship('User')
    content = db.relationship('Content', uselist=False)

    def __repr__(self):
        return '<post {} {}>'.format(self.id, self.title)

    __str__ = __repr__


class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    post_id = db.Column(db.BigInteger, db.ForeignKey('post.id'))
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<content {}>'.format(self.id)

    __str__ = __repr__
