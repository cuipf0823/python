# !/usr/bin/python
# coding=utf-8

import os
from app import create_app
from flask_script import Manager


app = create_app(os.getenv('CONFIG_NAME') or 'default')

manager = Manager(app)

'''
@manager.command
def test():
    """run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
<<<<<<< HEAD


=======
'''
>>>>>>> 825d30f510a36f6777c4ca295a1c4b081cb849da
if __name__ == '__main__':
    manager.run()
