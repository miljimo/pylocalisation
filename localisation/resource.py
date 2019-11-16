import os;
from localisation.__debug__    import __DEBUG__;
from localisation.dictionary   import  Dictionary;
from localisation.iresource    import  IResource;


"""
 The resource objects
"""
class Resource(IResource):

    def __init__(self, **kwargs):
        filename   = kwargs['filename'] if('filename' in kwargs) else "";
        
        if(os.path.exists(filename) != True):
            raise FileNotFoundError("File not found ={0}".format(filename));
        self.__Filename             = filename;
        self.__MergeResources       = Dictionary(item_class = Resource);
        self.__Resources            = dict();

    @property
    def Filename(self):
        return self.__Filename;
  
    def Get(self, key):
        result  = None;
        if(key in self.__Resources):
            result =  self.__Resources[key];
        if(result == None):
            if(len(self.Merges) > 0):
                result  =  self.__FindInMergeResources(key);
        return result;
    
    @property
    def Merges(self):
        return self.__MergeResources;

    def Add(self, key , resource):
        status  = False;
        if(type(key)  == str):
            if(resource != None):
                if(key in self.__Resources) != True:
                    self.__Resources[key] = resource;
                    status  = True;
        return status;

    def Remove(self, key):
        status  =  False;
        if(key in self.__Resources):
            del self.__Resources[key];
            status  = True;
        return status;
    
    @property
    def Count(self):
        return self.__MergeResources.Count;
    
    def __FindInMergeResources(self, key):
        result  = None;
        for resource_key in self.Merges:
            resource   = self.Merges.Get(resource_key);
            result     = resource.Get(key);            
            if(result != None):
                break;
        return result;


if(__name__ =="__main__"):
    ENABLE_TESTING = True;
    if(ENABLE_TESTING):
        try:
            resource         = Resource(filename  = "test/res.json");
            app_test         = resource.Get('app.text.name');
            password_text    = resource.Get('login.password');
            username         = resource.Get("app.register.form.firstname");
            another          = resource.Get("base.title.width");
            __DEBUG__("Username =  {0}".format(username));
            __DEBUG__("Password =  {0}".format(password_text));
            __DEBUG__("Application Title  =  {0}".format(app_test));
            __DEBUG__("another =  {0} ".format(another));
            print("Done")
           
        except Exception as err:
            __DEBUG__(err);
            __DEBUG__("testing application ended");
            print(err)
            
    

    
    
