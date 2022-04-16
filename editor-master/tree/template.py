import logging
from antlr4 import *
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Trees import Trees
from ASTgrammarLexer import ASTgrammarLexer
from ASTgrammarParser import ASTgrammarParser
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
    n = t.getChildCount()
    logging.info(counter, '[label = "', left.replace('"','\\"'), '"]', sep='', file=f)
    for i in range(0, n):
        right = t.getChild(i)
        nxt = next(gen)
        if right.getChildCount() == 0:
            logging.info(nxt, '[label = "', right.getText().replace('"','\\"'), '"]', sep='', file=f)
            logging.info(counter, '->', nxt, sep='', file=f)
        else:
            logging.info(nxt, '[label = "', names[right.getRuleIndex()], '"]', sep='', file=f)
            logging.info(counter, '->', nxt, sep='', file=f)
            node2diagram(t.getChild(i), names[right.getRuleIndex()].replace('"','\\"'), names, f, nxt, gen)


def tree2diagram(t, names):
    f = open("ASTgrammar.dot", "w")
    logging.info("digraph {", sep='', file=f)

    gen = (x for x in range(100000))

    node2diagram(t, names[t.getRuleIndex()], names, f, next(gen), gen)

    logging.info("}", sep='', file=f)
    f.close()

def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = ASTgrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ASTgrammarParser(stream)
    errorListener = ChatErrorListener()
    parser.addErrorListener(errorListener)
    tree = parser.t()
    # ast = syntaxVisitor().visitRulelist(tree)
    # print(tree.toStringTree(recog=parser))
    # print(parser.ruleNames)
    # print(toPrettyTree(tree, parser.ruleNames))
    # print(tree.toStringTree(recog=parser))
    tree2diagram(tree, parser.ruleNames)
    # print(parser.ruleNames[tree.getChild(0).getRuleIndex()], " ", parser.ruleNames)


if __name__ == '__main__':
    main(sys.argv)
