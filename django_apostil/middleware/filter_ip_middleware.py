from django.core.exceptions import PermissionDenied
from apostil.base import white_ip_range

# white_range = [f"10.24.12.{x}" for x in range(254)]

class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in white_ip_range:
            raise PermissionDenied

        response = self.get_response(request)

        return response