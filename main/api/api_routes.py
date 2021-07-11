from flask import jsonify, url_for, request, redirect
from . import api
from main.models import URL_Class
from main import db
''' in `create_short` & `retrieve_long` I implemented
	POST when parameters (url) is sent in http body.
	If we want to send parameters in query strings,
	then look at the bottom
'''

@api.before_app_first_request
def creation_db():
	db.create_all()

@api.route('/<string:link>')
def get_short_ver(link):
	obj = URL_Class.query.filter_by(short_url=link).first_or_404()
	obj.times_visited += 1
	db.session.commit()
	return redirect(obj.long_url)

def bad_response():
	return {'message': "URL isn't provided"}

@api.route('/long', methods=['POST'])
def create_short():
	link = request.get_json('url')

	if link is None:
		return jsonify(bad_response())

	link = link['url']
	res = URL_Class.query.filter_by(long_url=link).first()
	if res is not None:
		return jsonify({'message': 'such link already exist',
						'long url': res.long_url,
						'short_url': res.short_url})

	obj = URL_Class(long_url=link)
	db.session.add(obj)
	db.session.commit()
	return jsonify({'url-short': url_for('api.get_short_ver',
					link=obj.short_url, _external=True)})

@api.route('/short', methods=['POST'])
def retrieve_long():
	link = request.get_json('url')
	if link is None:
		return jsonify(bad_response())

	link = link['url']
	exist_url = URL_Class.query.filter_by(short_url=link[-5:]).first()
	if not exist_url:
		return jsonify({'message': 'No such short link in db'})

	return jsonify({'url-long': exist_url.long_url})

@api.route('/info', methods=['GET'])
def info():
	data = URL_Class.query.order_by(URL_Class.times_visited.desc()).all()
	return jsonify(Result=[d.serialize for d in data]), 201

# as query string
@api.route('/longQuery', methods=['POST'])
def create_short_query():
	link = request.args.get('url', None)

	if link is None or len(link) == 0:
		return jsonify(bad_response())

	res = URL_Class.query.filter_by(long_url=link).first()
	if res is not None:
		return jsonify({'message': 'such link already exist',
						'long url': res.long_url,
						'short_url': res.short_url})

	obj = URL_Class(long_url=link)
	db.session.add(obj)
	db.session.commit()
	return jsonify({'url-short': obj.short_url})

@api.route('/shortQuery', methods=['POST'])
def retrieve_long_query():
	link = request.args.get('url', None)

	if link is None:
		return jsonify(bad_response())

	exist_url = URL_Class.query.filter_by(short_url=link[-5:]).first()
	if not exist_url:
		return jsonify({'message': 'No such short link in db'})

	return jsonify({'url-long': exist_url.long_url})
