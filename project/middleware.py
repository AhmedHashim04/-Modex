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


class CPUMeasureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_cpu = time.process_time()
        response = self.get_response(request)
        end_cpu = time.process_time()

        cpu_time = end_cpu - start_cpu
        response["X-CPU-Time"] = f"{cpu_time:.6f}"
        return response


class FullCPUMeasureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_cpu = time.process_time()

        response = self.get_response(request)

        end_cpu = time.process_time()

        cpu_time = end_cpu - start_cpu
        response["X-CPU-Full-Time"] = f"{cpu_time:.6f}"
        return response
