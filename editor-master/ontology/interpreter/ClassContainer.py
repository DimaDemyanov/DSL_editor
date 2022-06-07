from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser

from interpreter.containers_util import *
from interpreter.AttrContainer import *

class ClassContainer:
    def __init__(self, name, attrs, opers):
        self.name = name
        self.attrs = attrs
        self.opers = opers

def class_context_to_class_container(class_):
    n = class_.getChildCount()
    name = ''
    attrs = []
    for i in range(n):
        child = class_.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.AttrContext):
            attrs.append(attr_context_to_attr_container(child))

    class_container = ClassContainer(name, attrs, [])
    return class_container