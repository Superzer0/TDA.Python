import getopt
import logging
import sys

from objects.InputParams import InputParams
from services.AFWordsClustering import AFWordsClustering
from services.ExecutionTime import LoggingTime
from services.FileService import ProcessingFilesService


def get_input_params(argv):
    """
    Reads cmd provided parameters for ProcessingEntry
    """
    input_file_path = 'console/example_dataset/example.txt'
    output_file_path = 'console/example_dataset/example_output.txt'
    compute_silhouette = True
    affinity_preference_factor = 'auto'

    try:
        opts, args = getopt.getopt(argv, "i:o:p:s:a:", ["ifile=", "ofile="])
    except getopt.GetoptError as e:
        logging.error("Invalid params! Try: -i <inputfile> -o <outputfile> -s <True|False "
                      "- compute silhouette coefficient> -a <affinity_preference_factor>")
        logging.error(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-i', "--ifile"]:
            input_file_path = arg
        elif opt in ['-o', '--ofile']:
            output_file_path = arg
        elif opt in ['-s']:
            compute_silhouette = arg == "True"
        elif opt in ['-a']:
            affinity_preference_factor = arg

    return InputParams(input_file_path, output_file_path, compute_silhouette, affinity_preference_factor)


def log_coefficient(coefficient):
    """
    Logs Silhouette coefficient that was computed
    """
    if coefficient:
        logging.info("Silhouette Coefficient: %0.3f" % coefficient)


def run():
    """
    Runs AF clustering processing using AFWordsClustering and FileService as a cmd app
    """
    logging.info("Started processing with following params" + str(sys.argv[1:]))
    input_params = get_input_params(sys.argv[1:])
    file_service = ProcessingFilesService(input_params, AFWordsClustering.is_word_eligible())
    input_data_dic = file_service.get_data()
    af_clustering = AFWordsClustering(input_data_dic, input_params.affinity_preference)
    results = af_clustering.process(input_params.compute_silhouette)
    file_service.save_results(results.processing_dictonary_results)
    log_coefficient(results.silhouette_coefficient)


if __name__ == "__main__":
    with LoggingTime("Total run time: "):
        run()
