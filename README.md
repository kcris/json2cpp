# json2cpp

## python script that generates c++ mapping classes for a given json

The typical c++ json parser library, loads json values into a map(string->variant), which discards all static checking that might be done by a compiler and that is error prone at runtime.

If a well known, fixed json format is used (taken from a json sample), direct mapping to c++ classes/members (preserving types) will allow typesafe client code.

## About
* generates c++ (11) classes with json load/save methods
* each json object in our sample becomes a c++ class, each json property of such an object becomes a c++ class member
* generated code still relies on a third party json parser library, currently [cpprest](https://github.com/Microsoft/cpprestsdk)
* json arrays must be homogeneous (all elements must have same 'type')
* the original script is available [here](https://gist.github.com/soharu/5083914). (no subobjects supported)
