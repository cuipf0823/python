# !/usr/bin/python
# coding=utf-8

import os
from app import create_app
from flask_script import Manager


if __name__ == '__main__':
    app = create_app(os.getenv('CONFIG_NAME') or 'default')
    manager = Manager(app)
    manager.run()
