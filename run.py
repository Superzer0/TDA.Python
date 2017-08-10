from console.af_cluster import run
from services.ExecutionTime import LoggingTime

if __name__ == "__main__":
    with LoggingTime("Total run time: "):
        run()
