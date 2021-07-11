from flask import (Blueprint, request,
					render_template, jsonify)


err = Blueprint('errors', __name__)
''' if user puts wrong url ->
	this error  will handle it
'''


@err.app_errorhandler(404)
def err_404(err):
	if request.accept_mimetypes.accept_json and\
	not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'page not found'})
		response.status_code = 404
		return response
	return render_template('errors/404.html'), 404
