from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

from interpreter.MArgContainer import *
from interpreter.MResContainer import *

class AggrContainer:
    def __init__(self, name, m_args, m_ress):
        self.name = name
        self.m_args = m_args
        self.m_ress = m_ress

def aggr_context_to_aggr_container(aggr):
    n = aggr.getChildCount()
    name = ''
    m_args = []
    m_ress = []
    for i in range(n):
        child = aggr.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.M_argContext):
            m_args.append(m_arg_context_to_m_arg_container(child))

        if isinstance(child, ontologyParser.M_resContext):
            m_ress.append(m_res_context_to_m_res_container(child))

    aggr_container = AggrContainer(name, m_args, m_ress)
    return aggr_container