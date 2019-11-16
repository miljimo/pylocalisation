
class IResource(object):

    def __init__(self):
        raise NotImplementedError("@IResource is an interface class");

    def Add(self, key, value):
         raise NotImplementedError("@Add method not implement.");

    def Get(self, key):
        raise NotImplementedError("@Get method must be implement");

    @property
    def Count(self):
        raise NotImplementedError("@Count : must be implemented");
    
    def Remove(self, key):
        raise NotImplementedError("@Remove method must be implemnt");

    @property
    def Merges(self):
        raise NotImplementedError("@Merges :Merges must be implement");

    @property
    def Filename(self):
        raise NotImplementedError("@Filename property must be implement");
