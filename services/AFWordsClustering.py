import logging

import distance
import numpy as np
import sklearn.cluster
from sklearn import metrics
from stemming.porter2 import stem

from objects.AFProcessingResults import AFProcessingResults
from objects.InputParams import InputParams
from services.ExecutionTime import LoggingTime


class AFWordsClustering:
    def __init__(self, data_dic, affinity_preference):
        self.__affinity_preference = affinity_preference
        self.__data_dic = data_dic

    def process(self, count_coefficient=False):
        reversed_stem_dic = {}
        with LoggingTime("Words stem dictionary prep took: "):
            for key, data in self.__data_dic.items():
                data.stem = stem(data.org)  # stemming words to discard noise from the data
                if data.stem in reversed_stem_dic:
                    stemmed_data = reversed_stem_dic[data.stem]
                    stemmed_data.append(data)
                else:
                    reversed_stem_dic[data.stem] = [data]

        logging.info("Preparing distance matrix...")

        with LoggingTime("Distance matrix  prep took: "):
            words = np.asarray(
                [data.stem for keys, data in self.__data_dic.items()])  # So that indexing with a list will work
            lev_similarity = -1 * np.array([[distance.sorensen(w1, w2) for w1 in words] for w2 in words])

        # to limit number of cluster we use min value from similarity matrix
        dynamic_preference = self.get_preference(lev_similarity, self.__affinity_preference)
        damping_factor = .9

        affinity_propagation_algorithm = sklearn.cluster.AffinityPropagation(affinity="precomputed",
                                                                             damping=damping_factor, max_iter=10000,
                                                                             verbose=True,
                                                                             preference=dynamic_preference)

        logging.info("Starting affinity propagation alg with damping %f and preference %s..."
                     % (damping_factor, str(dynamic_preference)))

        with LoggingTime("affinity propagation alg took "):
            af_results = affinity_propagation_algorithm.fit(lev_similarity)

            logging.info(
                "Affinity propagation alg finished. Estimated number of clusters: %d. \n Collecting and saving "
                "results... " % len(af_results.cluster_centers_indices_))

        for cluster_id in np.unique(af_results.labels_):
            exemplar = words[af_results.cluster_centers_indices_[cluster_id]]
            cluster = np.unique(words[np.nonzero(af_results.labels_ == cluster_id)])
            for cluster_entry in cluster:
                data_array = reversed_stem_dic[cluster_entry]
                for data_item in data_array:
                    data_item.group = cluster_id
                    if cluster_entry == exemplar:
                        data_item.isExemplar = True

        silhouette_coefficient = None
        if count_coefficient:
            with LoggingTime("Silhouette Coefficient computing took: "):
                logging.info("Computing Silhouette Coefficient ...")
                silhouette_coefficient = metrics.silhouette_score(lev_similarity, af_results.labels_,
                                                                  metric='precomputed')

        return AFProcessingResults(self.__data_dic, af_results, lev_similarity, silhouette_coefficient)

    @staticmethod
    def get_preference(lev_similarity, affinity_preference):
        if affinity_preference == InputParams.AFFINITY_PREFERENCE_AUTO:
            return None
        elif affinity_preference == InputParams.AFFINITY_PREFERENCE_DYNAMIC:
            minimal_dissimilarity = np.amin(lev_similarity)
            dynamic_preference = minimal_dissimilarity - (np.amax(lev_similarity) - minimal_dissimilarity)
            return dynamic_preference
        else:
            try:
                return abs(int(affinity_preference)) * -1
            except Exception as e:
                logging.warning(e)
                logging.warning(affinity_preference)
                return None

    @staticmethod
    def is_word_eligible():
        def word_eligibility(word):
            return len(stem(word.strip())) > 0

        return word_eligibility
