from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser

from interpreter.containers_util import *

class AttrContainer:
    def __init__(self, typeName, name):
        self.typeName = typeName
        self.name = name

def attr_context_to_attr_container(attr):
    n = attr.getChildCount()
    type_name = None
    name = ''
    for i in range(n):
        child = attr.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.Type_nameContext):
            type_name = name_to_str(child)

    attr_container = AttrContainer(type_name, name)
    return attr_container
