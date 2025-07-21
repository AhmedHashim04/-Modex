import logging
from django_ratelimit.exceptions import Ratelimited
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RatelimitLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            logger.warning(
                f"Ratelimited request from IP: {get_client_ip(request)} "
                f"User: {getattr(request.user, 'username', 'Anonymous')} "
                f"Path: {request.path}"
            )
        return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
