from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *


class EnumContainer:
    def __init__(self, name, constants):
        self.name = name
        self.constants = constants

def enum_context_to_enum_container(enum):
    n = enum.getChildCount()
    name = ''
    constants = []
    for i in range(n):
        child = enum.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.StringContext):
            constants.append(name_to_str(child))

    return EnumContainer(name, constants)
