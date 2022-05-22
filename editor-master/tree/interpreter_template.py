from antlr4 import *
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Trees import Trees
from (grammarName)Lexer import (grammarName)Lexer
from (grammarName)Parser import (grammarName)Parser
from antlr4.error.ErrorListener import *

class ChatErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception('line ' + str(line) + ':' + str(column) + ':' + msg)


level = 0

def toPrettyTree(t, ruleNames):
    global level
    level = 0
    return process(t, ruleNames).replace("(?m)^\\s+$", "").replace("\\r?\\n\\r?\\n", "\n")

def process(t, ruleNames):
    global level
    if t.getChildCount() == 0:
        return escapeWhitespace(Trees.getNodeText(t, ruleNames), False)
    sb = ""
    sb += lead(level)
    level += 1
    s = escapeWhitespace(Trees.getNodeText(t, ruleNames), False)
    sb += (s + ' ')
    for i in range(t.getChildCount()):
        sb += process(t.getChild(i), ruleNames)
    level -= 1
    # sb += lead(level)
    return sb

def lead(level):
    sb = ""
    if (level > 0):
        sb += "\n"
        for cnt in range(level):
            sb += " "
    return sb

def node2diagram(t, left, names, f, counter, gen):
    result = ''
    n = t.getChildCount()
    result = result + str(counter) + '[label = "' + left.replace('"','\\"') + '"]' + '\n'
    for i in range(0, n):
        right = t.getChild(i)
        nxt = next(gen)
        if right.getChildCount() == 0:
            result = result + str(nxt) + '[label = "' + right.getText().replace('"','\\"') + '"]'  + '\n'
            result = result + str(counter) + '->' + str(nxt)  + '\n'
        else:
            result = result + str(nxt) + '[label = "' + names[right.getRuleIndex()] + '"]'  + '\n'
            result = result + str(counter) + '->' + str(nxt)  + '\n'
            result = result + node2diagram(t.getChild(i), names[right.getRuleIndex()].replace('"','\\"'), names, f, nxt, gen)
    return result

def tree2diagram(t, names):
    with open("(grammarName).dot", "wb") as f:
        result = ''
        result = result + "digraph {\n"

        gen = (x for x in range(100000))

        result = result + node2diagram(t, names[t.getRuleIndex()], names, f, next(gen), gen)

        result = result + '}\n'
        f.write(result.encode('UTF-8'))

def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = (grammarName)Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = (grammarName)Parser(stream)
    errorListener = ChatErrorListener()
    parser.addErrorListener(errorListener)
    tree = parser.(firstNode)()
    # ast = syntaxVisitor().visitRulelist(tree)
    # print(tree.toStringTree(recog=parser))
    # print(parser.ruleNames)
    # print(toPrettyTree(tree, parser.ruleNames))
    # print(tree.toStringTree(recog=parser))
    tree2diagram(tree, parser.ruleNames)
    # print(parser.ruleNames[tree.getChild(0).getRuleIndex()], " ", parser.ruleNames)


if __name__ == '__main__':
    main(sys.argv)
