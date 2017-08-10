class ProcessingEntry:
    def __init__(self, org):
        self.__org = org
        self.__stem = org
        self.__group = -1
        self.__is_exemplar = False

    @property
    def org(self):
        """Original input word"""
        return self.__org

    @property
    def stem(self):
        """Stem version of original input word"""
        return self.__stem

    @stem.setter
    def stem(self, value):
        self.__stem = value

    @property
    def group(self):
        """group label set by AF algorithm"""
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value

    @property
    def is_exemplar(self):
        """True if word is centroid for its cluster"""
        return self.__is_exemplar

    @is_exemplar.setter
    def is_exemplar(self, value):
        self.__is_exemplar = value
