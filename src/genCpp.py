from genTools import *

#
# c++ parser library specific stuff
#
cppTypeMappings = {
    JsonElemType.BOOL : {
        'typename': 'bool',
        'load': 'as_bool',
        'save': 'web::json::value::boolean'
    },
    JsonElemType.NUMBER : {
        'typename': 'double',
        'load': 'as_double',
        'save': 'web::json::value::number'
    },
    JsonElemType.STRING : {
        'typename': 'std::wstring',
        'load': 'as_string',
        'save': 'web::json::value::string'
    },
    JsonElemType.ARRAY : {
        'typename': 'std::vector',
        'load': 'as_array',
        'save': 'web::json::value::array'
    },
    JsonElemType.OBJECT : {
        'typename': 'class',
        'load': 'as_object',
        'save': 'web::json::value::object'
    }
}
cppJsonVariantType = "web::json::value"

def membersList(varinfo, obj = None):
    members = []
    for info in varinfo:
        memberName = 'm_' if obj is None else '{}.m_'.format(obj)
        memberName += formatIdentifier(info[2] if len(info) >= 3 and info[0] != JsonElemType.OBJECT else info[1])
        members.append(memberName)
    return ", ".join(members)
    
def cppMember(info):
    if info[0] == JsonElemType.OBJECT: #json object
        return formatIdentifier(info[1])
    elif info[0] == JsonElemType.ARRAY: #json array
        return formatIdentifier(info[2])
    else: #simple type
        return formatIdentifier(info[1])

def jsonElemAt(info):
    memberName=cppMember(info)
    if memberName=='': #toplevel value
        return 'm_jsonValue'
    else:
        return 'm_jsonValue.at(L"{}")'.format(memberName)

def cppType(info):
    typeName=cppTypeMappings[info[0]]['typename']
    if info[0] == JsonElemType.OBJECT: #json object
        return formatTypename(info[1].title())
    elif info[0] == JsonElemType.ARRAY: #json array
        itemType = "{}Item".format(info[2].title()) if info[1] == JsonElemType.OBJECT else cppTypeMappings[info[1]]['typename']
        return '{}<{}>'.format(typeName, formatTypename(itemType))
    else: #simple type
        return formatTypename(typeName)


def cppGet(info):
    getter='try{\n'
    if info[0] == JsonElemType.OBJECT: #json object
        getter+='\t\t\treturn {}({});'.format(cppType(info), jsonElemAt(info))
    elif info[0] == JsonElemType.ARRAY: #json array
        getter+='\t\t\t{} arr;\n'.format(cppType(info))
        getter+='\t\t\tfor (const {} & item : {}.{}())\n'.format(cppJsonVariantType, jsonElemAt(info), cppTypeMappings[info[0]]['load'])

        if info[1] == JsonElemType.OBJECT: #array of objects
            elem='{}Item(item)'.format(formatIdentifier(info[2].title())) #array of objects
        else: #array of simple
            elem='item.{}()'.format(cppTypeMappings[info[1]]['load']) #simple array

        getter+='\t\t\t\tarr.push_back({});\n'.format(elem)
        getter+='\t\t\treturn arr;'
    else: #simple type
        getter+='\t\t\treturn {}.{}();'.format(jsonElemAt(info), cppTypeMappings[info[0]]['load'])
    getter+='\n\t\t}\n\t\tcatch(web::json::json_exception &) {\n\t\t\treturn defaultValue; //missing data\n\t\t}'
    return getter

def cppSet(info):
    setter=''
    if info[0] == JsonElemType.OBJECT: #json object
        setter+='{} = x.m_jsonValue; //json object'.format(jsonElemAt(info))
    elif info[0] == JsonElemType.ARRAY: #json array
        setter+='{}<{}> arr;\n'.format(cppTypeMappings[info[0]]['typename'], cppJsonVariantType)
        setter+='\t\tfor (const auto & item : x)\n'

        if info[1] == JsonElemType.OBJECT: #array of objects
            setter+='\t\t\tarr.push_back(item.m_jsonValue); //json objects\n'
        else: #array of simple
            setter+='\t\t\tarr.push_back({}(item));\n'.format(cppTypeMappings[info[1]]['save'])

        setter+='\t\t{} = {}(arr);'.format(jsonElemAt(info), cppTypeMappings[info[0]]['save'])
    else: #simple type
        setter+='{} = {}(x);'.format(jsonElemAt(info), cppTypeMappings[info[0]]['save'])
    return setter

#
# generate output class - c++
#
def generate_class(classname, data, exportedClass, deps):

    includes, varinfo = generate_variable_info(classname, data)
    varinfo.sort()

    dependentClasses = '' if deps==None else deps

    decl=''

    #begin class definition
    decl+='\n\n/*\n * struct {}\n */\nstruct {} {}\n'.format(classname, exportedClass, classname)
    decl+='{\n'

    #constructors
    decl+='\t{}() = default;\n'.format(classname) #explicitly defaulted ctor (force compiler generated default-ctor since the user ctor below otherwise inhibits it)
    decl+='\t{}(const {} & jsonValue) : m_jsonValue(jsonValue) {{}}\n\n'.format(classname, cppJsonVariantType)

    #make tuple - useful for implementing operator==, operator< if we have multiple data members in class; NOTE: might require c++17
    #decl+='\tauto tuple() const {{\n\t\treturn std::make_tuple({});\n\t}}\n\n'.format(membersList(varinfo))
    
    #member methods
    for info in varinfo:
        typeName=cppType(info)
        memberName=cppMember(info)
        if (memberName == ''):
            decl+='\t//toplevel value\n' #toplevel value - comment
            memberName='value'
        else:
            decl+='\t//{}\n'.format(memberName) #member - comment
            decl+='\t{} get_{}_json() const /*throw(web::json::json_exception)*/ {{\n\t\treturn {};\n\t}}\n'.format(cppJsonVariantType, memberName, jsonElemAt(info)) #getter (variant, may throw)

        decl+='\t{} get_{}(const {} & defaultValue = {}()) const throw() /*noexcept*/ {{\n\t\t{}\n\t}}\n'.format(typeName, memberName, typeName, typeName, cppGet(info)) #getter (getOrElse, typesafe, non throwable)
        decl+='\tvoid set_{}(const {} & x) {{\n\t\t{}\n\t}}\n'.format(memberName, typeName, cppSet(info)) #setter

        if info[0] == JsonElemType.OBJECT: #json object
            dependentClasses = generate_class(info[1].title(), info[2], exportedClass, dependentClasses) #recursively generate related classes
        elif info[0] == JsonElemType.ARRAY: #json array
            if info[1] == JsonElemType.OBJECT: 
                dependentClasses = generate_class("{}Item".format(info[2].title()), info[3][0], exportedClass, dependentClasses) #recursively generate related classes
        else: #simple type
          if not typeName is None:
            pass

    #end class definition
    decl+='\n\t//public data\n'
    decl+='\t{} m_jsonValue;\n'.format(cppJsonVariantType) #json value member
    decl+='};\n'

    print("Generated class: {}".format(classname))

    if deps==None:
        out='//\n// {}Json.h\n'.format(classname)
        out+='//\n// -- generated file, do NOT edit\n//\n'
        out+='#pragma once\n\n'
        out+='#include <cppRest/json.h> //json serialization library\n\n'
        #for i in range(len(includes)):
        #    out+="#include "{}.h" //generated\n".format(includes[i])
        out+='namespace {}Json {{'.format(classname)
        out+=dependentClasses+decl+'\n'
        out+='}} //namespace {}Json\n'.format(classname)
        return out

    return dependentClasses+decl
