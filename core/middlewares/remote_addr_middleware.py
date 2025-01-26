from django.http import HttpRequest

class RemoteAddrMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the ip_address attribute on the current request object.
        request.ip_address = request.META['REMOTE_ADDR']
        response = self.get_response(request)
        return response
