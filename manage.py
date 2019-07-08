from app import app, db
from flask_script import Manager, Server
from app.blog.models import User, Post

manager = Manager(app)

manager.add_command("server", Server())


@manager.shell
def make_shell_content():
    return dict(
        app=app,
        db=db,
        User=User,
        Post=Post
    )


if __name__ == '__main__':
    manager.run()
