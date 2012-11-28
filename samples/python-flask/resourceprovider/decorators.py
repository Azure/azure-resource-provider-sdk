from functools import wraps
from flask import request, current_app

def log_request_body(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		current_app.logger.debug("Request method: %s\nRequest args: %s \nRequest path: %s \nRequest body:%s\n" % (request.method, args, request.path,request.data))
		return f(*args, **kwargs)
	return decorated_function