import datetime
import functools
import logging
import time

logger = logging.getLogger(__name__)


class stopwatch:
    """Log run time with custom log info message. Use as decorator or as context manager"""

    def __init__(self, log_msg, caller_class=None):
        self.start_time = None
        if caller_class:
            self.msg = f"<{caller_class}> {log_msg}"
        else:
            self.msg = log_msg

    def __call__(self, function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)

        return wrapper

    def __enter__(self):
        logger.info(f"Starting: {self.msg}")
        self.start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.perf_counter()
        run_time = end_time - self.start_time
        logger.info(f"Finished: {self.msg} after {datetime.timedelta(seconds=run_time)}")
