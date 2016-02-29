#!/user/bin/env python

import json
import os
import sys
from types import *
#from collections import OrderedDict

def cpp_type(value):
    if isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'double'
    elif isinstance(value, str):
        return 'std::wstring'
    elif isinstance(value, list):
        return 'std::vector'
    elif isinstance(value, dict):
        return 'class' #'std::map' #TODO - anonymous class (in array?) ??
    else: #dict?
        #print("unsupported type {}".format(type(value)))
        pass #return None

def generate_variable_info(data):
    includes = []
    varinfo = []
    for k, v in list(data.items()):    
        if isinstance(v, list): #json array
            #if not 'vector' in includes:
            #    includes.append('#include <vector>')
            if isinstance(v[0], dict):
                includes.append('#include "{}Item.h" //generated'.format(k.title()))
                varinfo.append((cpp_type(v), cpp_type(v[0]), k, v))
            else:
                varinfo.append((cpp_type(v), cpp_type(v[0]), k))
        elif isinstance(v, dict): #json object
            if not k in includes:
                includes.append('#include "{}.h" //generated'.format(k))
            varinfo.append(('class',k, data[k]))
        else: #simple type
            typename = cpp_type(v)
            varinfo.append((typename, k))
            #if 'string' in typename and not 'string' in includes:
            #    includes.append('#include <string>')
    return includes, varinfo

# c++ parser library specific stuff
type_json_cpp = "web::json::value"
type_methods_load = {'int':'as_integer',               'bool':'as_bool',                   'double':'as_double',                'std::wstring':'as_string'}
type_methods_save = {'int':'web::json::value::number', 'bool':'web::json::value::boolean', 'double':'web::json::value::number', 'std::wstring':'web::json::value::string'}

def assign_statement_load(t, v):
    return 'm_{} = jsonObject.at(L"{}").{}();'.format(v, v, type_methods_load[t])

def assign_statement_save(t, v):
    return 'jsonObject[L"{}"] = {}(m_{});'.format(v, type_methods_save[t], v)

def array2vector_statements(elemt, var):
    stats = []
    stats.append('\n\t\tfor (const {} & item : jsonObject.at(L"{}").as_array())'.format(type_json_cpp, var))
    if elemt == 'class':
        stats.append('\tm_{}.push_back({}(item)); //json objects'.format(var, "{}Item".format(var.title()))) #array of objects
    else:
        stats.append('\tm_{}.push_back(item.{}());'.format(var, type_methods_load[elemt])) #simple array
    return stats

def vector2array_statements(elemt, var):
    stats = []
    temp = 't_'+ var
    stats.append('\n\tstd::vector<{}> {};'.format(type_json_cpp, temp))
    stats.append('for (const auto & item : m_{})'.format(var))
    if elemt == 'class': #array of objects
        stats.append('\t{}.push_back(item.save()); //json objects'.format(temp))
    else: #simple array
        stats.append('\t{}.push_back({}(item));'.format(temp, type_methods_save[elemt]))
    stats.append('jsonObject[L"{}"] = web::json::value::array({});'.format(var, temp))
    return stats

def membersList(varinfo, obj = None):
    members = []
    for info in varinfo:
        memberName = 'm_' if obj is None else '{}.m_'.format(obj)
        memberName += info[2] if len(info) >= 3 and info[0] != "class" else info[1]
        members.append(memberName)
    return ", ".join(members)
    
# generate output .h
def generate_header(classname, includes, varinfo, dirname):
    f = open(dirname + '/' + classname + '.h', 'wt')
    f.write('//\n// {}.h\n'.format(classname))
    f.write('//\n// -- generated file, do NOT edit\n//\n')
    f.write('#pragma once\n\n')
    f.write('#include <cppRest/json.h> //cpprest library used for json serialization\n\n')
    for i in range(len(includes)):
        f.write("{}\n".format(includes[i]))
    #class definition
    f.write('\n\nstruct {}\n'.format(classname))
    f.write('{\n')
    #constructors
    f.write('\t//constructors\n')
    f.write('\t{}() = default;\n'.format(classname)) #explicitly defaulted ctor (force compiler generated default-ctor since the user ctor below otherwise inhibits it)
    f.write('\t{}(const {} & jsonObject) : {}() {{ load(jsonObject); }}\n\n'.format(classname, type_json_cpp, classname)) #user ctor
    #operators
    f.write('\t//operators (see std::rel_ops)\n')
    f.write('\tbool operator==(const {} & other) const;\n'.format(classname))
    #f.write('\tbool operator!=(const {} & other) const {{ return !(*this == other); }}\n'.format(classname)) #see std::rel_ops instead
    f.write('\tbool operator<(const {} & other) const;\n\n'.format(classname))
    #load/save methods
    f.write('\t//json parsing and serializing\n')
    f.write('\tbool load(const {} & jsonObject);\n'.format(type_json_cpp))
    f.write('\t{} save() const;\n\n'.format(type_json_cpp))
    #data members
    f.write('\t//member data\n')
    for info in varinfo:
        if len(info) >= 3:
            if info[0] == "class": #json object
                f.write('\t{} m_{};\n'.format(info[1].title(), info[1]))
            else: #json array
                itemType = "{}Item".format(info[2].title()) if info[1] == "class" else info[1]
                f.write('\t{}<{}> m_{};\n'.format(info[0], itemType, info[2]))
        elif len(info) == 2: #simple type
            f.write('\t{} m_{};\n'.format(info[0], info[1]))
    f.write('};\n')

# generate output .cpp
def generate_source(classname, varinfo, dirname):
    f = open(dirname + '/' + classname + '.cpp', 'wt')
    f.write('//\n// {}.cpp\n'.format(classname))
    f.write('//\n// -- generated class for jsoncpp\n//\n')
    f.write('#include \"{}.h\"\n\n'.format(classname))
    #operators
    f.write('//equals operator\n')
    f.write('bool {}::operator==(const {} & other) const\n'.format(classname, classname))
    f.write('{\n')
    f.write('\treturn\n\t\tstd::tie({})\n\t\t==\n\t\tstd::tie({});\n'.format(membersList(varinfo), membersList(varinfo, "other")))
    f.write('}\n\n')
    f.write('//lessThan operator\n')
    f.write('bool {}::operator<(const {} & other) const\n'.format(classname, classname))
    f.write('{\n')
    f.write('\treturn\n\t\tstd::tie({})\n\t\t<\n\t\tstd::tie({});\n'.format(membersList(varinfo), membersList(varinfo, "other")))
    f.write('}\n\n')
    #load method:
    f.write('// parse\n')
    f.write('bool {}::load(const {} & jsonObject)\n'.format(classname, type_json_cpp))
    f.write('{\n')
    f.write('\ttry\n\t{\n') #try
    for info in varinfo:
        if len(info) >= 3:
            if (info[0] == "class"): #json object
                f.write('\t\tm_{}.load(jsonObject.at(L"{}")); //json object\n'.format(info[1], info[1]))                
                generate(info[1].title(), info[2], dirname) #recursively generate related classes
            elif 'vector' in info[0]: #json array
                for line in array2vector_statements(info[1], info[2]):
                    f.write('\t\t'+line+'\n')
                if info[1] == "class": 
                    generate("{}Item".format(info[2].title()), info[3][0], dirname) #recursively generate related classes
        elif len(info) == 2: #simple type
          if not info[0] is None:
            f.write('\t\t'+assign_statement_load(info[0], info[1])+'\n')
    f.write('\t}\n\tcatch(web::json::json_exception &) { return false; }\n') #catch
    f.write('\n\treturn true;\n}\n\n')
    #save method
    f.write('// serialize\n')
    f.write('{} {}::save() const\n'.format(type_json_cpp, classname))
    f.write('{\n')
    f.write('\t{} jsonObject;\n\n'.format(type_json_cpp))
    for info in varinfo:
        if len(info) >= 3:
            if (info[0] == "class"): #json object
                f.write('\tjsonObject[L"{}"] = m_{}.save(); //json object\n'.format(info[1], info[1]))
            elif 'vector' in info[0]: #json array
                for line in vector2array_statements(info[1], info[2]):
                    f.write('\t'+line+'\n')
        elif len(info) == 2: #simple type
          if not info[0] is None:
            f.write('\t'+assign_statement_save(info[0], info[1])+'\n')
    f.write('\n\treturn jsonObject;\n')
    f.write('}\n')

# generate output files
def generate(classname, data, dirname):
    includes, varinfo = generate_variable_info(data)
    varinfo.sort()
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)
    generate_header(classname, includes, varinfo, dirname)
    generate_source(classname, varinfo, dirname)
    print("Generated class: {}".format(classname))

#entry point
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('Usage: {} <json file>'.format(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    classname = filename.split('.')[0]
    try:
        with open(filename) as f:
            content = f.read()
    except IOError:
        print ("Can't open/read file".format(filename))
        sys.exit(2)
    data = json.loads(content) #data = json.loads(content, object_pairs_hook=OrderedDict)
    generate(classname.title(), data, "out." + classname)
    sys.exit(0)

#
# based on https://gist.github.com/soharu/5083914
#
# Generate c++(11) mapping classes for the object(s) inside a given json file. 
# Each data member of a generated class is mapped onto an existing json property.
# Note: the json is actually loaded/saved using an external library (cpprest).
#
# Warning: json arrays must be homogeneous
#
