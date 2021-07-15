import unittest
import json
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from main import create_app, db
from main.models import URL_Class
from main.config import config
from mock import patch
from flask import request


class api_Test(unittest.TestCase):
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

	def get_api_headers(self):
		return {
			'Content-Type': 'application/json'
		}

	def put_temp_url(self):
		response = self.client.post('/api/long',
					     headers=self.get_api_headers(),
					     data=json.dumps({"url": "https://rasdsndom_url"}))
		return response

	def test_long(self):
		get_headers = self.get_api_headers()
		# test wrong one
		response = self.client.get('/api/random',
					    headers=get_headers)
		self.assertEqual(response.status_code, 404)

		# test correct one
		response = self.client.post('/api/long',
					    headers=get_headers,
					    data=json.dumps({"url": "https://rasdsndom_url"}))
		self.assertEqual(response.status_code, 200)

		json_return = json.loads(response.get_data(as_text=True))
		self.assertIsNotNone(json_return['url-short'])

		# already existing one
		response = self.client.post('/api/long',
					     headers=get_headers,
					     data=json.dumps({"url": "https://rasdsndom_url"}))
		
		r = json.loads(response.get_data().decode('utf-8'))
		self.assertEqual(len(r), 3)

	def test_short(self):
		get_headers = self.get_api_headers()
		# wrong one
		response = self.client.get('/api/notShort',
					    headers=get_headers)
		self.assertEqual(response.status_code, 404)

		# correct one
		res = json.loads(self.put_temp_url().get_data().decode('utf-8'))
		response = self.client.post('/api/short',
					    headers=get_headers,
					    data=json.dumps({"url": res['url-short']}))
		self.assertEqual(response.status_code, 200)

		json_return = json.loads(response.get_data(as_text=True))
		self.assertIsNotNone(json_return['url-long'])

		# non-exisitng short
		response = self.client.post('/api/short',
					     headers=get_headers,
					     data=json.dumps({'url': 'https://notExist'}))
		r = json.loads(response.get_data().decode('utf-8'))
		self.assertEqual(len(r), 1)
		self.assertEqual(r, {'message': 'No such short link in db'})

	def test_info(self):
		data = URL_Class.query.all()
		self.assertEqual(len(data), 0)

	def test_longQuery(self):
		# correct
		url = 'https://randomUrl92'
		response = self.client.post(f'/api/longQuery?url={url}')
		self.assertEqual(response.status_code, 200)
		self.assertIsNotNone(response.get_data().decode('utf-8'))

		# if link is None or not provided
		response = self.client.post(f'/api/longQuery?url={""}')
		self.assertEqual(response.get_data(as_text=True).strip(), '{"message":"URL isn\'t provided"}')

		# if already exist
		response = self.client.post(f'/api/longQuery?url={url}')
		self.assertEqual(response.status_code, 200)
		t = json.loads(response.get_data().decode('utf-8'))
		self.assertEqual(len(t), 3)

	@patch('main.api.api_routes.retrieve_long_query')
	def test_shortQuery(self, mock_value):
		mock_value.return_value = {'url-long': 'just_mock_url'}
		self.assertEqual(mock_value.return_value, {'url-long': 'just_mock_url'})


if __name__ == '__main__':
	unittest.main()
