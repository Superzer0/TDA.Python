class InputParams:
    """Contains data for processing"""

    def __init__(self, input_file_path, output_file_path):
        if not input_file_path:
            raise ValueError("Input file path should not be empty")

        if not output_file_path:
            raise ValueError("Output file path should not be empty")

        self._input_file_path = input_file_path
        self._output_file_path = output_file_path

    @property
    def input_file_path(self):
        """Input file path for processing results"""
        return self._input_file_path

    @property
    def output_file_path(self):
        """Output file path for processing results"""
        return self._output_file_path
