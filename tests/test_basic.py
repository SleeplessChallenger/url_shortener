import unittest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from main import create_app, db
from flask import current_app
from main.config import config


class OverallTest(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['test_url'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_function(self):
		self.assertTrue(current_app is not None)
		self.assertFalse(current_app is None)


if __name__ == '__main__':
	unittest.main()
