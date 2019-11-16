DEBUG_MODE       = True;
DEBUG_LEVEL      = 0;

def __DEBUG__(*args, **kwargs):
    if(DEBUG_MODE):
        level   = kwargs['level'] if('level' in kwargs) else 0;
        if(level >= DEBUG_LEVEL):
            if(len(args) > 0):
                print(args[0]);


