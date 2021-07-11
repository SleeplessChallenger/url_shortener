import unittest
from flask import session

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from main import create_app, db
from main.models import URL_Class
from main.config import config


class routes_Test(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['test_url'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client(use_cookies=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_home_page(self):
		# GET requests
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/noPage')
		self.assertEqual(response.status_code, 404)

		# POST request
		# create new url
		response = self.client.post('/',
									data={
										'long_url': 'https://random_url'
									})
		self.assertEqual(response.status_code, 302)	

		# check of existing url gives long in response
		url = URL_Class.query.filter_by(long_url='https://random_url').first()
		response = self.client.post('/',
									data={
										'short_url': url.short_url
									})

		# if long_url already in db
		response = self.client.post('/',
									data={
										'long_url': 'https://random_url'
									})
		self.assertEqual(response.status_code, 302)

		# if put non-exisiting url
		response = self.client.post('/',
							data={
								'short_url': 'randomQ56'
							})
		self.assertNotEqual(response.status_code, 404)

	def test_sessions(self):
		with self.app.test_client() as c:
			with c.session_transaction() as s:
				s['long_url'] = 'https://random_url'
				s['short_url'] = 'https://k5v'

			self.assertIsNotNone(s['long_url'])
			self.assertEqual(s['short_url'], 'https://k5v')

	def test_info(self):
		data = URL_Class.query.all()
		self.assertEqual(len(data), 0)


if __name__ == '__main__':
	unittest.main()
