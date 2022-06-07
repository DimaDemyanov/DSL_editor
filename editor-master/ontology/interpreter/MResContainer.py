from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

from interpreter.MultContainer import *

class MResContainer:
    def __init__(self, type_name, name, mult):
        self.type_name = type_name
        self.name = name
        self.mult = mult

def m_res_context_to_m_res_container(m_arg):
    n = m_arg.getChildCount()
    type_name = None
    name = ''
    mult = None
    for i in range(n):
        child = m_arg.getChild(i)
        if isinstance(child, ontologyParser.Type_nameContext):
            type_name = name_to_str(child)

        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.MultContext):
            mult = mult_context_to_mult_container(child)

    return MResContainer(type_name, name, mult)