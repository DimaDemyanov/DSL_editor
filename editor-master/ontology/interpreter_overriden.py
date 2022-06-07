# That file was generated automatically with DSL editor
# The moment of generation: 27/05/2022 16:51:12
import os
from enum import Enum

from antlr4 import *
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Trees import Trees
from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
from antlr4.error.ErrorListener import *

from interpreter.ClassContainer import *
from interpreter.ActContainer import *
from interpreter.AggrContainer import *
from interpreter.EnumContainer import *
from Package_overriden import Package


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
    with open("ontology.dot", "wb") as f:
        result = ''
        result = result + "digraph {\n"

        gen = (x for x in range(100000))

        result = result + node2diagram(t, names[t.getRuleIndex()], names, f, next(gen), gen)

        result = result + '}\n'
        f.write(result.encode('UTF-8'))

class FileContainer:
    def __init__(self, packages):
        self.packages = packages


def file_context_to_file_container(file_):
    n = file_.getChildCount()
    packages = []
    for i in range(n):
        child = file_.getChild(i)
        if isinstance(child, ontologyParser.PackageContext):
            packages.append(package_context_to_package_container(child))
    file_container = FileContainer(packages)
    return file_container

class PackageContainer:
    def __init__(self, name, types, classes, enums, rels):
        self.name = name
        self.types = types
        self.classes = classes
        self.enums = enums
        self.rels = rels

def package_context_to_package_container(package):
    n = package.getChildCount()
    name = ''
    types = None
    enums = []
    classes = []
    rels = []
    for i in range(n):
        child = package.getChild(i)
        if isinstance(child, ontologyParser.Name_Context):
            name = name_to_str(child)

        if isinstance(child, ontologyParser.TypesContext):
            if types is None:
                types = types_context_to_types_container(child)
            else:
                print('Error: There are 2 types in one package!')

        if isinstance(child, ontologyParser.Enum_Context):
            enums.append(enum_context_to_enum_container(child))

        if isinstance(child, ontologyParser.Class_Context):
            classes.append(class_context_to_class_container(child))

        if isinstance(child, ontologyParser.RelContext):
            rels = rel_context_to_rel_container(child)
    package_container = PackageContainer(name, types, classes, enums, rels)
    return package_container


class RelContainer:
    def __init__(self, acts, assocs, gens, aggrs, comps, deps, impls):
        self.acts = acts
        self.assocs = assocs
        self.gens = gens
        self.aggrs = aggrs
        self.comps = comps
        self.deps = deps
        self.impls = impls

def rel_context_to_rel_container(rel):
    n = rel.getChildCount()
    # acts = []
    # assocs = []
    # gens = []
    # aggrs = []
    # comps = []
    # deps = []
    # impls = []
    rels = []

    for i in range(n):
        child = rel.getChild(i)
        if isinstance(child, ontologyParser.ActContext):
            rels.append(act_context_to_act_container(child))

        # if isinstance(child, ontologyParser.AssocContext):
        #     assocs.append(act_context_to_act_container(child))

        # if isinstance(child, ontologyParser.GenContext):
        #     gens.append(act_context_to_act_container(child))

        if isinstance(child, ontologyParser.AggrContext):
            rels.append(aggr_context_to_aggr_container(child))

        # if isinstance(child, ontologyParser.CompContext):
        #     comps.append(aggr_context_to_aggr_container(child))

        # if isinstance(child, ontologyParser.DepContext):
        #     deps.append(aggr_context_to_aggr_container(child))

        # if isinstance(child, ontologyParser.ImplContext):
        #     impls.append(aggr_context_to_aggr_container(child))

    return rels

class TypesContainer:
    def __init__(self, typeNames):
        self.typeNames = typeNames

def types_context_to_types_container(types):
    n = types.getChildCount()
    typeNames = []
    for i in range(n):
        child = types.getChild(i)
        if isinstance(child, ontologyParser.Type_nameContext):
            typeNames.append(name_to_str(child))

    tree_container = TypesContainer(typeNames)
    return tree_container



def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = ontologyLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ontologyParser(stream)
    errorListener = ChatErrorListener()
    parser.addErrorListener(errorListener)
    tree = parser.file_()
    # ast = syntaxVisitor().visitRulelist(tree)
    # print(tree.toStringTree(recog=parser))
    # print(parser.ruleNames)
    # print(toPrettyTree(tree, parser.ruleNames))
    # print(tree.toStringTree(recog=parser))
    # tree2diagram(tree, parser.ruleNames)
    # print(parser.ruleNames[tree.getChild(0).getRuleIndex()], " ", parser.ruleNames)
    file_container = file_context_to_file_container(tree)

    dir = os.path.join(os.path.dirname(__file__), 'output')
    if not os.path.exists(dir):
        os.mkdir(dir)
    for package in file_container.packages:
        with open(os.path.join(dir, package.name + '.json'), 'w', encoding="utf-8") as file:
            Package(file_container.packages[0], file).run()

    print('end')



if __name__ == '__main__':
    main(sys.argv)
