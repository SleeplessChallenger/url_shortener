from main import db
from flask import current_app, url_for
from datetime import datetime
import string
from random import choices
from sqlalchemy import desc


class URL_Class(db.Model):
	__tablename__ = 'urls'
	id = db.Column(db.Integer, primary_key=True)
	long_url = db.Column(db.String(450), nullable=False, unique=True)
	short_url = db.Column(db.String(10), unique=True, nullable=False)
	times_visited = db.Column(db.Integer, default='1')
	link_created = db.Column(db.DateTime, default=datetime.now)


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.short_url = self.get_short_ver()

	def __repr__(self):
		return f"long url:{self.long_url}; short ver:{self.short_url}"

	def get_short_ver(self):
		tokens = string.digits + string.ascii_letters
		# `ascii_letters` encompasses ascii_lowercase & ascii_uppercase
		short_url = ''.join(choices(tokens, k=5))

		if self.exists(short_url):
			# if exists, use recursion
			# to get valid one
			return self.get_short_ver()
		return short_url

	def exists(self, var):
		return self.query.filter_by(short_url=var).first()

	@property
	def serialize(self):
		return {
			'id': self.id,
			'long_url': self.long_url,
			'short_url': self.short_url,
			'times vis.': self.times_visited,
			'time created': self.link_created
		}
