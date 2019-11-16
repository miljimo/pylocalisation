import os;
import sys;
import json;
from events import EventHandler, Event;
from localisation.__debug__      import __DEBUG__;
from localisation.resource       import Resource;
from localisation.colour         import Colour;
from localisation.ibaseparser    import IBaseParser;
from localisation.parserregistry import ParserRegistry;
from localisation.parserevent    import ResourceEvent, ResourceParserEvent as ParserEvent;


class ResourceParser(IBaseParser):
    __RESOURCE_TYPES__                 = ['strings',
                                          'merge_resources',
                                          'colours']
    
    __ACCEPTED_STRING_FIELDS__         = ["key", "value"];
    __ACCEPTED_MERGE_RESOURCE_FLIEDS__ = ['filename']

    def __init__(self, **kwargs):
        filename  =  os.path.abspath(kwargs['filename']) if('filename' in kwargs) else None;
        if(os.path.exists(filename) != True):
            raise FileNotFoundError("File not found {0}".format(filename));
        self.__Filename = filename;
        self.__LoadedResources  = dict();
        self.__ResourceKeys     = dict();
        #Create events objects;
        self.__Progress    = EventHandler();
        self.__Loaded      = EventHandler();

    @property
    def Progress(self):
        return self.__Progress;
    
    @Progress.setter
    def Progress(self, handler):
        if(type(handler) == EventHandler):
            self.__Progress = handler;
            
    @property
    def Loaded(self):
        return self.__Loaded;
    
    @Loaded.setter
    def Loaded(self, handler):
        if(type(handler) == EventHandler):
            self.__Loaded = handler;
    
    def __ParserStrings(self, res_object, strings, filename):
        string_objects  = strings ;
        if(type(string_objects) != list):
            raise ValueError("@resource_parser: strings resource must be a list object of strings");
        
        for string_res in string_objects:
            for  key_string in string_res:
                if((key_string in self.__ACCEPTED_STRING_FIELDS__) != True):
                    raise ValueError("@resource_parser: unexpecting key_object resource found {0}".format(key_string));
            key  = string_res['key'];
            
            if(key in self.__ResourceKeys):
                raise ValueError("@resource_parser: resource key = [{0}] exist in {1} and {2}".format(key, self.__ResourceKeys[key], filename));
            res_object.Add(string_res['key'], string_res['value']);
            self.__ResourceKeys[key] = filename;
   
    def __ParserMergeResources(self, base_resource_object, resources, base_res_filename):        
        if(type(resources) != list):
            raise TypeError("resource_parser: merge_resource must be a list object []");
        
        for resource_res in resources:
            if(type(resource_res) != dict):
                raise TypeError("resource_parser: unexpected resource type provided {0}".format(resource_res));
                               
            if('filename' in resource_res) != True:
                raise ValueError("Merge resource object must have a filename");
            
            for field in resource_res:
                if(field in self.__ACCEPTED_MERGE_RESOURCE_FLIEDS__) != True:
                    raise ValueError("resource_parser : unexpected resource field = {0} in {1}".format(field, resource_res));

            filename   = resource_res['filename'];
            if(os.path.exists(filename) != True):
                # The user must be using a relative path
                dir_path         = os.path.dirname(os.path.realpath(base_res_filename));
                filename         = os.path.join(dir_path, filename);
                fullpath         = os.path.abspath(base_res_filename);
                currentFilePath  = os.path.abspath(filename);
                
                if(fullpath != currentFilePath):
                    resource_obj = self.__ParserResource(currentFilePath);
                    if(resource_obj != None):
                        base_resource_object.Merges.Add(currentFilePath, resource_obj);
                        
    """
     Parser function to 
    """
    def Parse(self):
        resource  = None;
        try:
            resource = self.__ParserResource(self.__Filename);            
            if (resource != None) and (self.Loaded != None):
                if(self.Loaded != None):
                    event  = ParserEvent(self, resource);
                    self.Loaded(event);
        except Exception as err:
            print("{0} Resource Type = ".format(type(resource)))
            __DEBUG__("@Stack trace in {0}".format(self.__Filename));
            raise err;       
        return resource;

    def __ParserColour(self, res_object, colour_res, filename):
        if(type(colour_res) != dict):
            raise TypeError(colour_res);
        if('key' in colour_res) != True:
            raise ValueError("@resource_parser: Expecting colour resource to have a key = {0}".format(colour_res));
            
        red     = colour_res['red']   if('red' in colour_res)   else 255;
        green   = colour_res['green'] if('green' in colour_res) else 255;
        blue    = colour_res['blue']  if('blue' in colour_res)  else 255;
        alpha   = colour_res['alpha'] if('alpha' in colour_res) else 255;
        key     = colour_res['key'];
        
        if(key in self.__ResourceKeys):
                raise ValueError("@resource_parser: resource key = [{0}] exist in {1} and {2}".format(key, self.__ResourceKeys[key], filename));        self.__ResourceKeys[key] = filename;
        colour  =  Colour(red  = red, green = green , blue = blue, alpha = alpha);
        res_object.Add(key, colour);
        
        
        pass;
    # Parser the resource list object of key type,

    def __ParserResourceObject(self, resource, key,  resource_list, filename):
       if(key == 'strings'):
             self.__ParserStrings(resource, resource_list, filename);
       elif(key == "colours"):
            for colour_res in  resource_list:
                self.__ParserColour(resource, colour_res, filename);
       elif(key  =='merge_resources'):
             self.__ParserMergeResources(resource,  resource_list, filename);
       else:
           raise ValueError("Unexpected resource tag element {0}".format(key));

    def __ParserResource(self, filename):
        resource  = None
        try:
            fullpath   = os.path.abspath(filename);
            
            if(os.path.exists(fullpath)):
                resource  = Resource(filename  = fullpath);
                
                if(fullpath in self.__LoadedResources) != True:
                    self.__LoadedResources[fullpath] = True;
                        
                    with open(fullpath , 'r') as stream:
                        jsobject  = json.load(stream);
                        
                        for key in jsobject:
                           if(key in self.__RESOURCE_TYPES__) != True:
                                raise ValueError("Unexpecting resource object found = {0}", key);
                           self.__ParserResourceObject(resource, key, jsobject[key], filename);
                        if(self.Progress != None):
                            self.Progress(ResourceEvent(self, filename));
           
        except Exception as err:
            __DEBUG__("@Stack trace in {0} :\n {1}".format(filename , err));
            raise  err;
       
        return resource;
        
        
# TEST CODES
if(__name__ == "__main__"):
    try:
        def OnProgress(event):
            __DEBUG__("Loading : {0}".format(event.Filename), level=2);

        def OnLoaded(event):
            __DEBUG__("Completed  Base File {0} ".format(event.Resource.Filename), level=2);
            
        parser    = ResourceParser(filename  =  "test/res.json");
        parser.Progress  += OnProgress;
        parser.Loaded    += OnLoaded;
        resource  =  parser.Parse();
        
        if(resource != None):
            app_test         = resource.Get('app.text.name');
            password_text    = resource.Get('login.password');
            username         = resource.Get("app.register.form.firstname");
            app              = resource.Get("App");
            another          = resource.Get("base.title.width");
            __DEBUG__(" App                = {0}".format(app));
            __DEBUG__(" Username           = {0}".format(username));
            __DEBUG__(" Password           = {0}".format(password_text));
            __DEBUG__(" Application Title  = {0}".format(app_test));
            __DEBUG__(" Merge Count        = {0}".format(len(resource.Merges)))
            __DEBUG__(" Resource Count     = {0}".format(resource.Count))
            __DEBUG__(" another            = {0}".format(another))
            __DEBUG__(" colour             = {0}".format(resource.Get("primary.colour.light")));
            __DEBUG__(" colour             = {0}".format(resource.Get("primary.colour")));
    except Exception as err:
        
        print(err, file=sys.stderr, flush = True);
        raise err;
    
        
