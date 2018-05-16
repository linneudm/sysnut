def add_variable_to_context(request):
	isAjax=False
	if request.is_ajax():
		isAjax=True

	return {'isAjax': isAjax}

class MyMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_response(self, request, response):
		if request.is_ajax():
			response['Location'] = request.get_full_path()
			response['Cache-Control'] = 'no-cache'
		return response;
