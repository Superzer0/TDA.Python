import logging
import sys

from console.af_cluster import run
from services.ExecutionTime import LoggingTime


def configure_logging():
    """Configures logging service"""
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s [%(levelname)-5.5s]  %(message)s")


if __name__ == "__main__":
    with LoggingTime("Total run time: "):
        configure_logging()
        run()
