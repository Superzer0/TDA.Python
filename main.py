import getopt
import sys
import distance
import numpy as np
import sklearn.cluster
from stemming.porter2 import stem
from objects.inputparams import InputParams
from objects.processing_entry import ProcessingEntry
from objects.execution_time_context import LoggingTime
import csv
from sklearn import metrics
import matplotlib.pyplot as plt
from itertools import cycle


def get_input_params(argv):
    input_file_path = 'example_names.txt'
    output_file_path = 'example_output.txt'
    generate_plot = False
    compute_silhouette = False
    affinity_preference_factor = 'dynamic'

    try:
        opts, args = getopt.getopt(argv, "i:o:p:s:a:", ["ifile=", "ofile="])
    except getopt.GetoptError as e:
        print("Invalid params! Try: -i <inputfile> -o <outputfile> -p <True|False "
              "- save plot> -s <True|False - compute silhouette coefficient> -a <affinity_preference_factor>")
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-i', "--ifile"]:
            input_file_path = arg
        elif opt in ['-o', '--ofile']:
            output_file_path = arg
        elif opt in ['-s']:
            compute_silhouette = arg == "True"
        elif opt in ['-p']:
            generate_plot = arg == "True"
        elif opt in ['-a']:
            affinity_preference_factor = arg

    return InputParams(input_file_path, output_file_path, generate_plot, compute_silhouette, affinity_preference_factor)


def get_data(in_params):
    with LoggingTime("Fetching data took "):
        try:
            with open(in_params.input_file_path, 'r', encoding="utf8") as csvFiles:
                reader = csv.reader(csvFiles, delimiter=',', quotechar='|')
                dictionary = {}
                for data in reader:
                    if len(data) > 1 and data[0] and data[1]:  # ignore malformed data lines
                        if word_is_eligible(data[1]):
                            dictionary[data[0]] = ProcessingEntry(data[0], data[1])
                return dictionary
        except IOError:
            print("IO Error has occurred. Check input file")
            raise
        except:
            print("Reading data failed. Check input file format")
            raise


def word_is_eligible(word):
    return len(word) <= 12 and len(stem(word.strip())) > 0


def process(data_dic, affinity_preference):
    reversed_stem_dic = {}
    with LoggingTime("Words stem dictionary prep took "):
        for key, data in data_dic.items():
            data.stem = stem(data.org.strip().lower())  # stemming words to discard noise from the data
            if data.stem in reversed_stem_dic:
                stemmed_data = reversed_stem_dic[data.stem]
                stemmed_data.append(data)
            else:
                reversed_stem_dic[data.stem] = [data]

    print("Preparing distance matrix...")

    with LoggingTime("Distance matrix  prep took "):
        words = np.asarray([data.stem for keys, data in data_dic.items()])  # So that indexing with a list will work
        lev_similarity = -1 * np.array([[distance.sorensen(w1, w2) for w1 in words] for w2 in words])

    # to limit number of cluster we use min value from similarity matrix
    dynamic_preference = get_preference(lev_similarity, affinity_preference)
    damping_factor = .9

    affinity_propagation_algorithm = sklearn.cluster.AffinityPropagation(affinity="precomputed",
                                                                         damping=damping_factor,
                                                                         verbose=True, preference=dynamic_preference)

    print("Starting affinity propagation alg with damping %f and preference %s..."
          % (damping_factor, str(dynamic_preference)))

    with LoggingTime("affinity propagation alg took "):
        af_results = affinity_propagation_algorithm.fit(lev_similarity)

    print("Affinity propagation alg finished. Estimated number of clusters: %d. \n Collecting and saving results..."
          % len(af_results.cluster_centers_indices_))

    for cluster_id in np.unique(af_results.labels_):
        exemplar = words[af_results.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(af_results.labels_ == cluster_id)])
        for cluster_entry in cluster:
            data_array = reversed_stem_dic[cluster_entry]
            for data_item in data_array:
                data_item.group = cluster_id
                if cluster_entry == exemplar:
                    data_item.isExemplar = True

    return data_dic, af_results, lev_similarity


def get_preference(lev_similarity, affinity_preference):
    if affinity_preference == 'auto':
        return None
    elif affinity_preference == 'dynamic':
        minimal_dissimilarity = np.amin(lev_similarity)
        dynamic_preference = minimal_dissimilarity - (np.amax(lev_similarity) - minimal_dissimilarity)
        return dynamic_preference
    else:
        try:
            return abs(int(affinity_preference)) * -1
        except Exception as e:
            print(e)
            print(affinity_preference)
            return None


def print_clustering_stats(af, x):
    print("Computing Silhouette Coefficient ...")
    with LoggingTime("Silhouette Coefficient computing took "):
        print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(x, af.labels_, metric='precomputed'))


def save_plot(af, distance_matrix, output_file_name):
    try:
        cluster_centers_indices = af.cluster_centers_indices_
        labels = af.labels_
        print("Generating plot...")
        n_clusters_ = len(cluster_centers_indices)

        plt.close('all')
        plt.figure(1)
        plt.clf()

        colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
        for k, col in zip(range(n_clusters_), colors):
            class_members = labels == k
            cluster_center = distance_matrix[cluster_centers_indices[k]]
            plt.plot(distance_matrix[class_members, 0], distance_matrix[class_members, 1], col + '.')
            plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=14)
            for x in distance_matrix[class_members]:
                plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.savefig('%s.png' % output_file_name, bbox_inches='tight')
        plt.savefig('%s.pdf' % output_file_name)
    except Exception as e:
        print(e)


def save_results(params, result_data):
    try:
        with open(params.output_file_path, 'w', newline='', encoding="utf8") as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',', quotechar='|')
            for key, entry in result_data.items():
                csv_writer.writerow([entry.id, entry.org, entry.stem, entry.group])
        print("Results saved in %s" % params.output_file_path)
    except IOError:
        print("IO Error when saving results")


def run():
    print("Started processing with following params" + str(sys.argv[1:]))
    input_params = get_input_params(sys.argv[1:])
    input_data_dic = get_data(input_params)
    print("Loaded data with %i entries with affinity preference factor: %s"
          % (len(input_data_dic), str(input_params.affinity_preference)))
    results, af_results, distance_matrix = process(input_data_dic, input_params.affinity_preference)
    save_results(input_params, results)

    if input_params.generate_plot:
        save_plot(af_results, distance_matrix, input_params.output_file_path)

    if input_params.compute_silhouette:
        print_clustering_stats(af_results, distance_matrix)


if __name__ == "__main__":
    with LoggingTime("Total run time: "):
        run()
