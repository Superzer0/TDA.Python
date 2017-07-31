class ProcessingEntry:
    def __init__(self, item_id, org):
        self.__id = item_id
        self.__org = org
        self.__stem = org
        self.__group = -1
        self.__is_exemplar = False

    @property
    def id(self):
        return self.__id

    @property
    def org(self):
        return self.__org

    @property
    def stem(self):
        return self.__stem

    @stem.setter
    def stem(self, value):
        self.__stem = value

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value

    @property
    def is_exemplar(self):
        return self.__is_exemplar

    @is_exemplar.setter
    def is_exemplar(self, value):
        self.__is_exemplar = value

