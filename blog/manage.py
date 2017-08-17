# !/usr/bin/python
# coding=utf-8

import os
from app import create_app
from flask_script import Manager
from .app.models import User, Post


app = create_app(os.getenv('CONFIG_NAME') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app, User=User, Post=post)

manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
