import os;
import json;

DEBUG_MODE       = True;
DEBUG_LEVEL      = 0;

def __DEBUG__(*args, **kwargs):
    if(DEBUG_MODE):
        level   = kwargs['level'] if('level' in kwargs) else 0;
        if(level >= DEBUG_LEVEL):
            if(len(args) > 0):
                print(args[0]);

class Resource(object):

    __PARSES_TYES__           = ['strings','merge_resources']
    __STRING_RES_FIELDS__     = ["key", "value"];
    __MERGE_RESOURCE_FLIEDS__ = ['filename']
    
    def __init__(self, **kwargs):
        self.__Filename             = kwargs['filename'] if('filename' in kwargs) else "";
        self.__MergeDictionaries    = dict();
        self.__Resources            = dict();
        self.__LoadResource();

    @property
    def Filename(self):
        return self.__Filename;

    def AddResource(self, resource):
        status  = False;
        
        if(isinstance(resource, Resource) != True):
            raise TypeError("Expecting a resource object");
        
        if((resource.Filename in self.__MergeDictionaries) != True):
            self.__MergeDictionaries[resource.Filename] = resource;
            status                                      =  True;
        return status;

    def RemoveResource(self, filename):
        status  = False;
        
        if(os.path.exists(filename)):
            if(filename in self.__MergeDictionaries):
                del self.__MergeDictionaries[filename];
                status  = True;
        return status;

    def GetResource(self, filename):
        resource  =  None;
        if(os.path.exists(filename)):
            if(filename in self.__MergeDictionaries):
                resource  = self.__MergeDictionaries[filename];
        return resource;
        

    def Get(self, key):
        result  = None;
        if(key in self.__Resources):
            result =  self.__Resources[key];
            
        if(result == None):
            if(self.MergeCount > 0):
                result  =  self.__FindInMergeResources(key);
        return result;
    
    @property
    def Resources(self):
        return self.__MergeDictionaries;

    def __FindInMergeResources(self, key):
        result  = None;
        for resource_key in self.Resources:
            resource   =self.Resources[resource_key];
            result   = resource.Get(key);            
            if(result != None):
                break;
        return result;
    
    @property
    def MergeCount(self):
        return len(self.Resources);

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
        return len(self.__Resources)

    def __LoadResource(self):
        try:
            if(os.path.exists(self.Filename) != True):
                raise FileNotFoundError("@resource_parser: resource file name [{0}] does not exist.".format(self.Filename));
            
            with open(self.Filename , 'r') as stream:
                jsobject  = json.load(stream);
                for key in jsobject:
                    if(key in self.__PARSES_TYES__) != True:
                        raise ValueError("Unexpecting resource object found = {0}", key);
                    
                    if(key == 'strings'):
                        # String Parser
                        string_objects  =  jsobject[key];
                        if(type(string_objects) != list):
                            raise ValueError("@resource_parser: strings resource must be a list object of strings");
                        for string_res in string_objects:
                            # Check if the fields that can be accepted are in the object
                             for  key_string in string_res:
                                if((key_string in self.__STRING_RES_FIELDS__) != True):
                                     raise ValueError("@resource_parser: unexpecting key_object resource found {0}".format(key_string));
                             self.Add(string_res['key'], string_res['value']);
                             
                    elif(key  =='merge_resources'):
                        #Merge the resource object
                        resources  =  jsobject[key];
                        if(type(resources) != list):
                            raise TypeError("resource_parser: merge_resource must be a list object []");
                        for resource_res in resources:
                            if(type(resource_res) != dict):
                                raise TypeError("resource_parser: unexpected resource type provided {0}".format(resource_res));
                            
                            if('filename' in resource_res) != True:
                                raise ValueError("Merge resource object must have a filename");
                            
                            for field in resource_res:
                                if(field in self.__MERGE_RESOURCE_FLIEDS__) != True:
                                    raise ValueError("resource_parser : unexpected resource field = {0} in {1}".format(field, resource));
                                
                            resource_obj  =  Resource(filename  =  resource_res['filename']);
                            if(resource_obj != None):
                                self.AddResource(resource_obj);
                                __DEBUG__("Resource {0} added".format(resource_obj.Filename));
                                
        except Exception as err:
            __DEBUG__("@Stack trace in {0}".format(self.Filename));
            raise err;
                            


if(__name__ =="__main__"):
    ENABLE_TESTING = True;
    if(ENABLE_TESTING):
        try:
            resource  = Resource(filename  = "test/res.json");
            app_test  = resource.Get('app.text.name');
            password_text = resource.Get('login.password');
            username      = resource.Get("app.register.form.firstname");
            __DEBUG__(username);
            __DEBUG__(password_text);
            __DEBUG__(app_test);
        except Exception as err:
            __DEBUG__(err);
            __DEBUG__("testing application ended", level = 1);
            raise;
    

    
    
