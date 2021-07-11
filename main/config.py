import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DB_URI') or\
		'sqlite:///' + os.path.join(basedir, 'urls.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY')


class TestDD:
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_urlDB.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY')


config = {
	'production': Config,
	'test_url': TestDD
}
