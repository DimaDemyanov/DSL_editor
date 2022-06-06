# That file was generated automatically with DSL editor
# The moment of generation: 27/05/2022 16:51:12


from antlr4 import *
from antlr4.Utils import escapeWhitespace
from antlr4.tree.Trees import Trees
from ontologyLexer import ontologyLexer
from ontologyParser import ontologyParser
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


def file_context_to_file_container(file_, file):
    n = file_.getChildCount()
    packages = []
    for i in range(n):
        child = file_.getChild(i)
        if isinstance(child, ontologyParser.PackageContext):
            packages.append(package_context_to_package_container(child, file))
    file_container = FileContainer(packages)
    return file_container

class PackageContainer:
    def __init__(self, types, classes, enum):
        self.types = types
        self.classes = classes
        self.enum = enum

def package_context_to_package_container(package, file):
    n = package.getChildCount()
    types = None
    enum = None
    classes = []
    for i in range(n):
        child = package.getChild(i)
        if isinstance(child, ontologyParser.TypesContext):
            if types is None:
                types = types_context_to_types_container(child, file)
            else:
                print('Error: There are 2 types in one package!')

        if isinstance(child, ontologyParser.Enum_Context):
            if enum is None:
                enum = enum_context_to_enum_container(child, file)
            else:
                print('Error: There are 2 enums in one package!')

        if isinstance(child, ontologyParser.Class_Context):
            classes.append(class_context_to_class_container(child, file))
    package_container = PackageContainer(types, classes, enum)
    return package_container

class EnumContainer:
    def __init__(self, name, constants):
        self.name = name
        self.constants = constants

def enum_context_to_enum_container(enum, file):
    pass

class ClassContainer:
    def __init__(self, name, constants):
        self.name = name
        self.constants = constants

def class_context_to_class_container(class_, file):
    pass

class TypesContainer:
    def __init__(self, typeNames):
        self.typeNames = typeNames

def types_context_to_types_container(types, file):
    n = types.getChildCount()
    typeNames = []
    for i in range(n):
        child = types.getChild(i)
        if isinstance(child, ontologyParser.Type_nameContext):
            typeNames.append(type_name_to_str(child))

    tree_container = TypesContainer(typeNames)
    return tree_container

def type_name_to_str(type_name):
    result = ''
    n = type_name.getChildCount()
    for i in range(n):
        child = type_name.getChild(i)
        result += child.symbol.text
    return result

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
    file_context_to_file_container(tree, 'out.dima')
    print('end')



if __name__ == '__main__':
    main(sys.argv)
