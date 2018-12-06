#!/user/bin/env python

import json
import os
import sys

from genTools import *
from genCpp import generate_class #custom generator for c++

#
# main - entry point
#
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('Usage: {} <json file> <export=''>'.format(sys.argv[0]))
        sys.exit(1)

    #read input json file
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            content = f.read()
    except IOError:
        print ("Can't open/read file".format(filename))
        sys.exit(2)
    data = json.loads(content) #data = json.loads(content, object_pairs_hook=OrderedDict)
    
    #generate output
    classname=formatIdentifier(filename.split('.')[0].title())
    exportedClass=sys.argv[2] if (len(sys.argv) == 3) else ''
    outputText = generate_class(classname, data, exportedClass, None) #custom generator for c++, see import at the top

    #write output source file
    dirname="out"
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)

    filename = dirname + '/' + classname + 'Json.h'
    print("Saving to file: {}\n\n{}".format(filename, outputText))

    f = open(filename, 'wt')
    f.write(outputText)
    f.flush
    f.close

#
# based on https://gist.github.com/soharu/5083914
#
# requires python 3 (tested with python 3.4)
#
# Generate c++(11) mapping classes for the elements inside a given json file. 
# Provide type-safe access to known json elements via c++ type/name checking.
#
# 1. For KNOWN json elements we provide safe access via getter/setter methods (compiler checked type and name of json element)
# 2. For ALL OTHER json elements we provide a public json (variant) value (useful for json elements that were not known at generation time)
#
# Warning: json arrays must be homogeneous. 
# Generator will handle a given array based on the first element of the array (as provided in the input json at generation time)
#
