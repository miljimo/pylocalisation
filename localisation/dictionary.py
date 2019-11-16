
class Dictionary(object):

    def __init__(self, **kwargs):
        self.__Items  =  dict();
        self.__cls    = kwargs['item_class'] if('item_class' in kwargs) else None;
 
    def __iter__(self):
        self.__startIndex = 0;
        self.__endIndex   = 0;
        return self;

    def __next__(self):
        item  = None;
        self.__endIndex  = self.Count - 1;
        if(self.__startIndex <= self.__endIndex):
            keys  = self.Keys;
            return keys[self.__startIndex]           
        else:
            raise StopIteration();

    def Add(self, key,  resource):
        status = False;
        if(type(key) != str):
            raise TypeError("Dictionary.key cannot be a null type");
        if(self.__cls != None):
            if(isinstance(resource, self.__cls) != True):
                raise TypeError("Expecting an type of {0} but this given {1}".format(type(self.__cls), type(resource)));
            if( key in self.__Items) != True:
                self.__Items[key] = resource;
                status  = True;
        else:
            if(key in self.__Items) != True:
                self.__Items[key] = resource;
                status = True;
        return status;

    def Insert(self, key , resource):
        status  = False;
        if(key ==  None) :
            raise TypeError("@Dictionary : key cannot be a null type");
        
        if(self.__cls != None):
            if(isinstance(resource, self.__cls)):
                if(key in self.__Items):
                    self.__Items[key] = resource; #replace
                else:
                    self.Add(self, key, resource);
                status  = True;
        else:
            self.__Items[key] = resource;
            status = True;       

        return status;

    def Remove(self, key):
        status  = False;
        if( key in self.__Items):
            del self.__Items[key];
            status  = True;
        return status;

    def Get(self, key):
        result  = None;
        if(key in self.__Items):
            result  =  self.__Items[key];
        return result;            
    
    @property
    def Keys(self):
        keys  =  list();
        for key in self.__Items:
            keys.append(key);
            
        return keys;

    def __len__(self):
        return self.Count;

    @property
    def Count(self):
        return len(self.__Items);
