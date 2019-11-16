class IBaseParser(object):

    def __init__(self,*args,  **kwargs):
        pass;
    
    def Parse(self):
        raise NotImplementedError("@Parser.Parse : method is not implemented");
