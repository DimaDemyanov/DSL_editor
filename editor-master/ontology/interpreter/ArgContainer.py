from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

class ArgContainer:
    def __init__(self, type_name, name):
        self.type_name = type_name
        self.name = name

def arg_context_to_arg_container(m_arg):
    n = m_arg.getChildCount()
    type_name = None
    name = ''
    for i in range(n):
        child = m_arg.getChild(i)
        if isinstance(child, ontologyParser.Type_nameContext):
            type_name = name_to_str(child)

        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

    return ArgContainer(type_name, name)