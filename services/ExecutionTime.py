"""ContextManager that logs time that elapsed between start and exit of inner statement"""

import logging
from time import time


class LoggingTime:
    def __init__(self, action_description):
        """Initialized LoggingTime class"""
        self.__action_description = action_description

    def __enter__(self):
        self.__time = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_elapsed = time() - self.__time
        logging.info("%s - %f seconds" % (self.__action_description, time_elapsed))
