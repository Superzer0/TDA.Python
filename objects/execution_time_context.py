from time import time


class LoggingTime:
    def __init__(self, action_description):
        self.__action_description = action_description

    def __enter__(self):
        self.__time = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_elapsed = time() - self.__time
        print("%s - %f seconds" % (self.__action_description, time_elapsed))
