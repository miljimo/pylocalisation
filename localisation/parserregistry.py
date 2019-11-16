class ParserRegistry(object):
    __RESOURCE_PARSERS = dict();

    def __init__(self):
        pass;


    def Add(self, type_key, clsParser):
        if(type(type_key) != str):
            raise TypeError("Add type_key must be string type {0}".format(type_key));
        if(clsParser != None):
            if((type_key in self.__RESOURCE_PARSERS) != True):
                self.__RESOURCE_PARSERS[type_key] = clsParser;
