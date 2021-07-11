import unittest
from unittest.mock import patch
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from main import create_app, db
from main.models import URL_Class
from main.config import config


class ModelTest(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['test_url'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.testURL = URL_Class(long_url='https://random_url')
		db.session.add(self.testURL)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_repr(self):
		short_url = self.testURL.short_url
		self.assertEqual(repr(self.testURL), f"long url:{self.testURL.long_url}; short ver:{short_url}")

	def test_times_visited(self):
		self.assertEqual(self.testURL.times_visited, 1)

	@patch('main.models.URL_Class.serialize')
	def test_serialize(self, mock_obj):
		short_url = self.testURL.short_url
		mock_obj.return_value = {
			'id': 1,
			'long_url': 'https://random_url',
			'short_url': short_url,
			'times vis.': 1,
		}
		self.assertEqual(mock_obj.return_value, {
				'id': self.testURL.id,
				'long_url': self.testURL.long_url,
				'short_url': short_url,
				'times vis.': 1
			})


if __name__ == '__main__':
	unittest.main()
