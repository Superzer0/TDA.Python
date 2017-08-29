"""AFProcessingResults contains results of the AF algorithm run"""


class AFProcessingResults:
    def __init__(self, data_dic, af_results, lev_similarity, silhouette_coef=None):
        """Initialize AFProcessingResults class"""
        self.__silhouette_coef = silhouette_coef
        self.__lev_similarity = lev_similarity
        self.__af_results = af_results
        self.__data_dic = data_dic

    @property
    def similarity_matrix(self):
        """Words similarity matrix"""
        return self.__lev_similarity

    @property
    def af_results(self):
        """Affinity propagation clustering results"""
        return self.__af_results

    @property
    def processing_dictonary_results(self):
        """Dictionary containing org_word, stem_word, clustered group_label"""
        return self.__data_dic

    @property
    def silhouette_coefficient(self):
        """silhouette coefficient computed for input set"""
        return self.__silhouette_coef
