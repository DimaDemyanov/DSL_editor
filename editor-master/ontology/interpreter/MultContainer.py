from enum import Enum

from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from interpreter.containers_util import *

class Mult(Enum):
    ZERO = 1
    ONE = 2
    ANY = 3
    ZERO_OR_ONE = 4
    ONE_OR_MORE = 5


def mult_context_to_mult_container(mult):
    n = mult.getChildCount()
    mult_count = None

    for i in range(n):
        child = mult.getChild(i)
        if isinstance(child, ontologyParser.Mult_cntContext):
            mult_count = mult_cnt_to_mult(child)

    return mult_count



def mult_cnt_to_mult(mult):
    result = ''
    n = mult.getChildCount()
    for i in range(n):
        child = mult.getChild(i)
        result += child.symbol.text

    if '0' == result:
        return Mult.ZERO
    if '1' == result:
        return Mult.ONE
    if '*' == result:
        return Mult.ANY
    if '0..1' == result:
        return Mult.ZERO_OR_ONE
    if '1..*' == result:
        return Mult.ONE_OR_MORE

    print('Error: no mult matched with ' + result)

    return None
