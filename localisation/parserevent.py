from events    import Event;
from localisation.iresource import IResource;


class ResourceEvent(Event):

    def __init__(self, sender, filename):
        super().__init__("resource.event");
        self.__Filename   =  filename;
        self.__Sender     =  sender;

    @property
    def Sender(self):
        return self.__Sender;
    
    @property
    def Filename(self):
        return self.__Filename;
    
class ResourceParserEvent(ResourceEvent):

    def __init__(self, sender, resource: IResource):       
        if(isinstance(resource, IResource) is not True):
            raise TypeError("@ResourceParserEvent: expecting a resource object");
        super().__init__(sender, resource.Filename);
        self.__Resource   = resource;
        
    @property
    def Resource(self):
        return self.__Resource;
    
  



