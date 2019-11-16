
from localisation.ibaseparser import IBaseParser;


class StringParser(IBaseParser):

    def __init__(self, **kwargs):
        self.__rawObjects  = kwargs['strings']
