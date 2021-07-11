from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired, Length, Email,
							   EqualTo, ValidationError, Regexp)
from .models import URL_Class


class LongToShort(FlaskForm):
	long_url = StringField('Long URL', validators=[DataRequired()])
	submit = SubmitField('Create Short Version!')

	def validate_no_long(self, long_url):
		link = URL_Class.query.filter_by(long_url=long_url.data).first()
		if link:
			raise ValidationError("Such link already in DB. Use another url to see result")


class ShortToLong(FlaskForm):
	short_url = StringField('Short URL', validators=[DataRequired()])
	submit = SubmitField('Get long version')

	def validate_long_exist(self, short_url):
		link = URL_Class.query.filter_by(short_url=short_url.data).first()
		if not link:
			raise ValidationError("No such short link in DB. Create it at first")
