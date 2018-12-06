from enum import IntEnum

class JsonElemType(IntEnum):
    BOOL = 1
    NUMBER = 2
    STRING = 3
    ARRAY = 4
    OBJECT = 5

def jsonType(value):
    if isinstance(value, bool):
        return JsonElemType.BOOL
    elif isinstance(value, int):
        return JsonElemType.NUMBER
    elif isinstance(value, float):
        return JsonElemType.NUMBER
    elif isinstance(value, str):
        return JsonElemType.STRING
    elif isinstance(value, list):
        return JsonElemType.ARRAY
    elif isinstance(value, dict):
        return JsonElemType.OBJECT
    else: #dict?
        #print("unsupported type {}".format(type(value)))
        pass #return None

def formatIdentifier(name):
    identifier = name
    if (len(identifier)>0 and identifier[0].isdigit()):
      identifier = "_" + identifier
    return identifier.replace(".", "_")

def formatTypename(name):
    return formatIdentifier(name)

def formatFilename(name):
    return formatIdentifier(name)

def generate_variable_info(classname, data):
    includes = []
    varinfo = []
    if  isinstance(data, dict): #json root is an object
        for k, v in list(data.items()):
            type=jsonType(v)
            if isinstance(v, list): #json array
                assert len(v) > 0, "input array must not be empty (we cannot determine the type of the elements inside)"
                elemType=jsonType(v[0])
                if isinstance(v[0], dict):
                    includes.append('{}Item'.format(formatFilename(k.title())))
                    varinfo.append((type, elemType, k, v))
                else:
                    varinfo.append((type, elemType, k))
            elif isinstance(v, dict): #json object
                if not k in includes:
                    includes.append('{}'.format(formatFilename(k)))
                varinfo.append((type, k, data[k]))
            else: #simple type
                varinfo.append((type, k))
    elif isinstance(data, list): #json root is an array
        type=jsonType(data)
        assert len(data) > 0, "input array must not be empty (we cannot determine the type of the elements inside)"
        elemType=jsonType(data[0])
        if isinstance(data[0], dict):
            includes.append('{}Item'.format(formatFilename(classname.title())))
            varinfo.append((type, elemType, '', data))
        else:
            varinfo.append((type, elemType, ''))

    return includes, varinfo
