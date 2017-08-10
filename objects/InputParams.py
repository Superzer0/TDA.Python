class InputParams:
    """Contains data for processing"""

    AFFINITY_PREFERENCE_AUTO = 'auto'  # preference will be set by an algorithm
    AFFINITY_PREFERENCE_DYNAMIC = 'dynamic'  # preference will be computed using similarity matrix

    def __init__(self, input_file_path, output_file_path,
                 compute_silhouette, preference_factor):
        if not input_file_path:
            raise ValueError("Input file path should not be empty")

        if not output_file_path:
            raise ValueError("Output file path should not be empty")

        self.__input_file_path = input_file_path
        self.__output_file_path = output_file_path
        self.__compute_silhouette = compute_silhouette
        self.__preference_factor = preference_factor

    @property
    def input_file_path(self):
        """Input file path for processing results"""
        return self.__input_file_path

    @property
    def output_file_path(self):
        """Output file path for processing results"""
        return self.__output_file_path

    @property
    def compute_silhouette(self):
        """If to compute silhouette coefficient"""
        return self.__compute_silhouette

    @property
    def affinity_preference(self):
        """Affinity propagation preference. Lower values result in fewer clusters"""
        return self.__preference_factor
