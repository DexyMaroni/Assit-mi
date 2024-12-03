import time
import logging

logger = logging.getLogger(__name__)

class MonitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        logger.info(f"Request {request.path} processed in {round((end_time - start_time) * 1000, 2)} ms")
        return response
