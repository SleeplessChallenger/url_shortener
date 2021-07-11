from flask import (Blueprint, render_template,
					redirect, flash, url_for, session)
from .forms import LongToShort, ShortToLong
from main import db
from main.models import URL_Class
from sqlalchemy import desc

# check validate_on_sumbit() 
url = Blueprint('url', __name__)

@url.before_app_first_request
def creation_db():
	db.create_all()

@url.route('/<string:link>')
def get_short_ver(link):
	obj = URL_Class.query.filter_by(short_url=link).first_or_404()
	obj.times_visited += 1
	db.session.commit()
	return redirect(obj.long_url)

def add_link(link):
	res = URL_Class.query.filter_by(long_url=link).first()
	if res is not None:
		return None

	newLink = URL_Class(long_url=link)
	# and the short version will be created automatically
	# as we have .get_short_ver() in models
	db.session.add(newLink)
	db.session.commit()
	return newLink

def retrieve_link(link):
	# we have check whether
	# the short link in db in
	# forms, but make here for safety
	obj = URL_Class.query.filter_by(short_url=link[-5:]).first()
	if not obj:
		return None

	obj.times_visited += 1
	db.session.commit()
	return obj

@url.route('/', methods=['GET', 'POST'])
def home():
	''' we use session to keep variables between routes.
		As we have 5 variables in short url, we'll
		check whether such short url in db with [-5:]
		(see `retrieve_link`. If no such short link found ->
		 redirection with alert)
	'''
	
	formLongShort = LongToShort()
	formShortLong = ShortToLong()

	# POST method
	if formLongShort.validate_on_submit():
		long_url = formLongShort.long_url.data.strip()
		result = add_link(long_url)
		if not result:
			flash('Such link already exist. Look here for all', 'danger')
			return redirect(url_for('url.info'))

		session['long_url'] = result.long_url
		session['short_url'] = result.short_url
		return redirect(url_for('url.get_short_result'))

	# POST method	
	if formShortLong.validate_on_submit():
		short_url = formShortLong.short_url.data.strip()
		result = retrieve_link(short_url)
		if not result:
			flash('No short link in db. Look here for all', 'danger')
			return redirect(url_for('url.info'))

		session['long_url'] = result.long_url
		session['short_url'] = result.short_url
		return redirect(url_for('url.get_long_result'))

	# GET method
	return render_template('two_forms.html', formOne=formLongShort,
											 formTwo=formShortLong)

@url.route('/resultShort')
def get_short_result():
	short_url = session.get('short_url', None)
	long_url = session.get('long_url', None)

	if short_url is None or long_url is None:
		flash('No urls found in session')
		return redirect(url_for('url.home'))

	return render_template('longToshort_urls.html',
							new_short=short_url,
							old_long=long_url)

@url.route('/resultLong')
def get_long_result():
	short_url = session.get('short_url', None)
	long_url = session.get('long_url', None)

	if short_url is None or long_url is None:
		flash('No urls found in session')
		return redirect(url_for('url.home'))

	return render_template('shortTolong_urls.html',
							long=long_url,
							short=short_url)

@url.route('/info', methods=['GET'])
def info():
	''' will display all the info about existing urls,
		but a) if already exisitng url is put -> flash() will
		display the error and show all info b) if short non-exisitng
		url is put -> flash() will display the error and show all info
	'''
	allData = URL_Class.query.order_by(URL_Class.times_visited.desc()).all()
	return render_template('info_urls.html', data=allData)
