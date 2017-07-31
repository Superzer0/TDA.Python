import getopt
import sys
import distance
import numpy as np
import sklearn.cluster
from stemming.porter2 import stem
from objects.inputparams import InputParams
from objects.processing_entry import ProcessingEntry


def get_input_params(argv):
    input_file_path = 'example_names.txt'
    output_file_path = 'example_output.txt'
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(" -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-i', "--ifile"]:
            input_file_path = arg
        elif opt in ['-o', '--ofile']:
            output_file_path = arg

    return InputParams(input_file_path, output_file_path)


def get_data(in_params):
    try:
        with open(in_params.input_file_path, 'r') as file:
            lines = file.read().splitlines()
            dictionary = {}
            for line in lines:
                data = line.split()
                dictionary[data[0]] = ProcessingEntry(data[0], data[1])

            return dictionary
    except IOError:
        print("IO Error has occurred. Check input file")
        raise
    except:
        print("Reading data failed. Check input file format")
        raise


def process(data_dic):
    reversed_stem_dic = {}
    for key, data in data_dic.items():
        data.stem = stem(data.org)  # stemming words to discard noise from the data
        if data.stem in reversed_stem_dic:
            stemmed_data = reversed_stem_dic[data.stem]
            stemmed_data.append(data)
        else:
            reversed_stem_dic[data.stem] = [data]

    words = np.asarray([data.stem for keys, data in data_dic.items()])  # So that indexing with a list will work
    lev_similarity = -1 * np.array([[distance.levenshtein(w1, w2) for w1 in words] for w2 in words])

    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        for cluster_entry in cluster:
            data_array = reversed_stem_dic[cluster_entry]
            for data_item in data_array:
                data_item.group = cluster_id
                if cluster_entry == exemplar:
                    data_item.isExemplar = True
                    # cluster_str = ", ".join(cluster)
                    # print(" - *%s:* %s" % (exemplar, cluster_str))
    return data_dic


def save_results(input_params, result_data):
    for key, entry in result_data.items():
        print("id: %s, word: %s, stem: %s, groupId: %s" % (entry.id, entry.org, entry.stem, entry.group))
        # output id stem version groupId
        # todo: save to file


if __name__ == "__main__":
    input_params = get_input_params(sys.argv[1:])
    input_data_dic = get_data(input_params)
    results = process(input_data_dic)
    save_results(input_params, results)
