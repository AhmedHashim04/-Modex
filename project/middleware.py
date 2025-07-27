import time
import logging

logger = logging.getLogger(__name__)

class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start
        logger.info(f"{request.path} took {duration:.4f}s")
        return response
