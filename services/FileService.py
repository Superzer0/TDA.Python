import csv
import logging

from objects.ProcessingEntry import ProcessingEntry
from services.ExecutionTime import LoggingTime


class ProcessingFilesService:
    """Manages I/O for clustering scripts"""

    def __init__(self, io_params, word_eligible_fun):
        self.__word_eligible_fun = word_eligible_fun
        self.__io_params = io_params

    def get_data(self):
        """Reads input file consisting of words to be clustered. One word per line"""
        with LoggingTime("Fetching data took: "):
            try:
                with open(self.__io_params.input_file_path, 'r', encoding="utf8") as csvFiles:
                    reader = csv.reader(csvFiles, delimiter=',', quotechar='|')
                    dictionary = {}
                    for data in reader:
                        if len(data) > 0 and data[0]:  # ignore malformed data lines
                            word_base = data[0].strip().lower()
                            if self.word_is_eligible(word_base) and word_base not in dictionary:
                                dictionary[word_base] = ProcessingEntry(word_base)
                    logging.info("Loaded %i search terms" % (len(dictionary)))
                    return dictionary
            except IOError as e:
                logging.error("IO Error has occurred. Check input file")
                logging.error(e)
                raise
            except:
                logging.error("Reading data failed. Check input file format")
                raise

    def save_results(self, result_data):
        """Saves clustering results in csv file. Example line: org_word, stem_word, cluster_label"""
        try:
            with open(self.__io_params.output_file_path, 'w', newline='', encoding="utf8") as csvFile:
                csv_writer = csv.writer(csvFile, delimiter=',', quotechar='|')
                items_count = 0
                for key, entry in result_data.items():
                    csv_writer.writerow([entry.org, entry.stem, entry.group])
                    items_count += 1
            logging.info("%i results saved in %s" % (items_count, self.__io_params.output_file_path))
        except IOError as e:
            logging.error("IO Error when saving results")
            logging.error(e)

    def word_is_eligible(self, word):
        return self.__word_eligible_fun(word)
