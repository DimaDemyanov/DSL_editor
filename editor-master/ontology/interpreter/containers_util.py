from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

def name_to_str(name):
    result = ''
    n = name.getChildCount()
    for i in range(n):
        child = name.getChild(i)
        result += child.symbol.text

    if isinstance(name, ontologyParser.Type_nameContext):
        result = result[1:-1]
    if isinstance(name, ontologyParser.Name_Context):
        result = result[1:-1]
    if isinstance(name, ontologyParser.StringContext):
        result = result[1:-1]
    return result