from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

from interpreter.ArgContainer import *
from interpreter.ResContainer import *

class ActContainer:
    def __init__(self, name, args, ress):
        self.name = name
        self.args = args
        self.ress = ress

def act_context_to_act_container(act):
    n = act.getChildCount()
    name = ''
    args = []
    ress = []
    for i in range(n):
        child = act.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.ArgContext):
            args.append(arg_context_to_arg_container(child))

        if isinstance(child, ontologyParser.ResContext):
            ress.append(res_context_to_res_container(child))

    return ActContainer(name, args, ress)