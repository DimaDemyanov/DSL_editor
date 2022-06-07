import os
import re
import shutil

from datetime import datetime

from antlr4 import *
from antlr4.error.ErrorListener import *
from graphviz import Source

from symantic.ciaoLexer import ciaoLexer
from symantic.ciaoParser import ciaoParser
from symantic.ciaoVisitor import ciaoVisitor

DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

class ChatErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception('line ' + str(line) + ':' + str(column) + ':' + msg)


def findSymanticName(symantic):
    regex = r"([A-Z][A-Z0-9_]*)"
    search = re.search(regex, symantic, re.MULTILINE | re.IGNORECASE)
    return search.group(1)


def createFiles(grammarName):
    if not os.path.exists(grammarName):
        os.mkdir(grammarName)


def makeTemplate(grammarName, firstNode):
    shutil.copyfile(
        os.path.join('tree', 'interpreter_template.py'),
        os.path.join(grammarName, 'interpreter.py'))
    with open(os.path.join(grammarName, 'interpreter.py'), 'r') as templateFile:
        s = templateFile.read()
    s = s.replace('(grammarName)', grammarName)
    s = s.replace('(firstNode)', firstNode)
    # add comments about automatic generation
    s = "# That file was generated automatically with DSL editor\n" + \
        f"# The moment of generation: {datetime.now().strftime(DATETIME_FORMAT)}\n\n\n" + s
    with open(os.path.join(grammarName, 'interpreter.py'), 'w') as f:
        f.write(s)


# no same var names
def check_same_var_names(program):
    var = program["var"]
    names = list(map(lambda x: x["name"], var))
    if len(names) != len(set(names)):
        return (-1, "Duplicates var names")
    return (0, "Ok")


# no same func names
def check_same_func_names(program, func):
    var = program[func]
    names = list(map(lambda x: x["name"] + str(len(x["value"])), var))
    if len(names) != len(set(names)):
        return (-1, "Duplicates " + func + " names")
    return (0, "Ok")


# parms in func cals = parms in func definitions
## TODO:  number count
def check_number_parms(program):
    states = program["state"]
    calls = []
    calls.extend(list(map(
    lambda x: x["condition"]["name"] + str(len(x["condition"]["value"]))
    if not isinstance(x["condition"], str) else "" , states)))
    calls.extend(list(map(
    lambda x: x["action"]["name"] + str(len(x["action"]["value"]))
    if not isinstance(x["action"], str) else "" , states)))
    calls = list(filter(lambda x: x != "", calls))
    names = []
    for name in ["required", "provided", "inner"]:
        names.extend(list(map(lambda x: x["name"] + str(len(x["value"])), program[name])))
    for call in calls:
        if call not in names:
            return (-1, call.rstrip('0123456789') + " is undefined")
    return (0, "Ok")


# check 'entry' occurs only once
# check nothing ends with 'entry'
def check_entry(program):
    states = program["state"]
    n = 0
    for state in states:
        if state["end"] == "entry" :
            return (-1, "tail of edge can't be entry state")
        if state["start"] == "entry" :
            n += 1
    if n < 1:
        return (-1, "entry state not found")
    # if n > 1:
    #     return (-1, "entry state occurs more than one time")
    return (0, "Ok")


# check nothing start with 'end'
def check_exit(program):
    states = program["state"]
    for state in states:
        if state["start"] == "exit" :
            return (-1, "head of edge can't be exit state")
    return (0, "Ok")


def checks(program):
    (code, text) = check_same_var_names(program)
    if code != 0:
        return (code, text)
    for name in ["required", "provided", "inner"]:
        (code, text) = check_same_func_names(program, name)
        if code != 0:
            return (code, text)
    (code, text) = check_number_parms(program)
    if code != 0:
        return (code, text)

    (code, text) = check_entry(program)
    if code != 0:
        return (code, text)

    (code, text) = check_exit(program)
    if code != 0:
        return (code, text)
    return (0, "Ok")


def get_graph(state):
    graph = {}
    for s in state:
        o = {
        "condition": 'True' if s['condition'] == "" else s['condition'],
        "action": s['action'],
        "end": s['end']
        }
        if s['start'] not in graph:
            graph.update({s['start']:[o]})
        else:
            graph[s['start']].append(o)
    # print(json.dumps(graph, indent=2))
    graph1 = {}
    for key, value in graph.items():
        ind = -1
        for i, node in enumerate(value):
            # print(node)
            if node["condition"] == "else":
                # print("HERE")
                ind = i
            if ind > -1:
                vvalue = value.copy()
                vvalue.append(vvalue.pop(ind))
                graph1[key] = vvalue
            else:
                graph1[key] = value.copy()
    return graph1


def make_python(graphs, symanticName):
    def add_todo_comment(spaces, file):
        print(spaces, "# TODO: add implementation", sep='', file=file)

    def add_header_comment(file):
        print("# That file was generated automatically with DSL editor", sep='', file=file)
        print(f"# The moment of generation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n", sep='', file=file)

    f = open(os.path.join(symanticName, symanticName + ".py"), "w")
    add_header_comment(f)

    for program in graphs:

        print(checks(program))

        name = program['name']
        var = program['var']
        required = program['required']
        provided = program['provided']
        inner = program['inner']
        query = program['query']
        state = program['state']

        indent = ''
        print(indent, "class ", name, ":", sep='', file=f)
        indent += '    '
        print("", sep='', file=f)

        print(indent, "#VARS", sep='', file=f)
        print(indent, "def __init__(self):", sep='', file=f)
        indent += '    '
        for v in var:
            print(indent, "self.", v["name"], " = ", v["value"],  sep='', file=f)
        print(indent, 'self.__state__ = "entry"', sep='', file=f)
        print("", sep='', file=f)
        indent = indent[:-4]

        print(indent, "#INNER", sep='', file=f)
        for i in inner:
            parms = ', '.join(["self"] + i["value"])
            print(indent, "def __", i["name"], "(", parms, "):",  sep='', file=f)
            indent += '    '
            add_todo_comment(indent, f)
            print(indent, "pass",  sep='', file=f)
            indent = indent[:-4]
            print("", sep='', file=f)

        print(indent, "#PROVIDED", sep='', file=f)
        for p in provided:
            parms = ', '.join(["self"] + p["value"])
            print(indent, "def ", p["name"], "(", parms, "):",  sep='', file=f)
            indent += '    '
            add_todo_comment(indent, f)
            print(indent, "pass",  sep='', file=f)
            indent = indent[:-4]
            print("", sep='', file=f)

        print(indent, "def run(self):", sep='', file=f)
        indent += '    '
        print(indent, "while (True):", sep='', file=f)
        indent += '    '
        print(indent, 'if self.__state__ == "exit":', sep='', file=f)
        indent += '    '
        print(indent, "break", sep='', file=f)
        indent = indent[:-4]

        graph = get_graph(state)

        for key, value in graph.items():
            print(indent, 'if self.__state__ == "', key, '" :', sep='', file=f)
            for v in value:
                indent += '    '
                condition = ""
                if isinstance(v["condition"], str):
                    condition = v["condition"]
                elif v["condition"]["name"] in [d['name'] for d in inner]:
                    condition = 'self.__' + v["condition"]["name"] + '(' + ', '.join(v["condition"]["value"]) + ')'
                else:
                    condition = v["condition"]["name"] + '(' + ', '.join(v["condition"]["value"]) + ')'
                action = ""
                if isinstance(v["action"], str):
                    action = v["action"]
                    if not action.replace(':=',' = self.__') == action:
                        action = 'self.' + action.replace(':=',' = self.__')
                elif v["action"]["name"] in [d['name'] for d in inner]:
                    print(v["action"]["name"])
                    action = 'self.__' + v["action"]["name"] + '(' + ', '.join(v["action"]["value"]) + ')'
                else:
                    print(v["action"]["name"])
                    action = v["action"]["name"] + '(' + ', '.join(v["action"]["value"]) + ')'
                end = v["end"]
                if condition != "else":
                    print(indent, 'if ', condition, ':', sep='', file=f)
                    indent += '    '
                if action != "":
                    print(indent, action, sep='', file=f)
                print(indent, 'self.__state__ = "', end, '"', sep='', file=f)
                print(indent, 'continue', sep='', file=f)
                if condition != "else":
                    indent = indent[:-4]
                indent = indent[:-4]
        indent = ""
        print("", sep='', file=f)
        print("", sep='', file=f)

    # print(indent, "if __name__ == '__main__':", sep='', file=f)
    # indent += '    '
    # print(indent, name, ".main()", sep='', file=f)
    # indent = indent[:-4]
    f.close()
    return 0


def buildDiagram(symantic):
    try:
        symanticName = findSymanticName(symantic)
    except Exception as m:
        print(m)
        print('file format error')
        return 'file format error', -1

    try:
        input = InputStream(symantic)
        lexer = ciaoLexer(input)
        stream = CommonTokenStream(lexer)
        parser = ciaoParser(stream)
        parser.removeErrorListeners()
        errorListener = ChatErrorListener()
        parser.addErrorListener(errorListener)
        tree = parser.p()
    except Exception as m:
        print(str(m))
        return str(m), -1

    try:
        createFiles(symanticName)
    except Exception as m:
        print(m)
        print('file system error')
        return 'file system error', -1

    try:
        v = ciaoVisitor()
        ast = v.visit(tree)
        graphs = v.get_graphs()
        for program in graphs:
            (code, error) = checks(program)
            if code != 0:
                return error, code
    except Exception as m:
        print(m)
        print('check error')
        return 'check error', -1

    try:
        v.print_dict(symanticName)
    except Exception as m:
        print(m)
        print('error while creating dot file')
        return 'error while creating dot file', -1

    try:
        graph = Source.from_file(os.path.join(symanticName, symanticName + '.dot'))
        graph.render(filename=symanticName, directory=symanticName, format='svg')
        target_path = 'public/diagram/' + symanticName + '.svg'
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copyfile(
            os.path.join(symanticName, symanticName + '.svg'),
            target_path)
    except Exception as m:
        print(m)
        print('error while creating png file')
        return 'error while creating png file', -1

    return 'diagram/' + symanticName + '.svg', 0

def removeComments(symantic):
    result = ''
    for line in symantic.splitlines():
        result = result + (line + '\n' if not line.lstrip().startswith('//') else '')

    return result

def buildCode(symantic):

    try:
        symanticName = findSymanticName(symantic)
    except Exception as m:
        print(m)
        print('file format error')
        return 'file format error', -1

    # symantic = removeComments(symantic)

    try:
        input = InputStream(symantic)
        lexer = ciaoLexer(input)
        stream = CommonTokenStream(lexer)
        parser = ciaoParser(stream)
        parser.removeErrorListeners()
        errorListener = ChatErrorListener()
        parser.addErrorListener(errorListener)
        tree = parser.p()
    except Exception as m:
        print(str(m))
        return str(m), -1

    try:
        createFiles(symanticName)
    except Exception as m:
        print(m)
        print('file system error')
        return 'file system error', -1

    try:
        v = ciaoVisitor()
        ast = v.visit(tree)
        graphs = v.get_graphs()
        for program in graphs:
            (code, error) = checks(program)
            if code != 0:
                return error, code
    except Exception as m:
        print(m)
        print('check error')
        return 'check error', -1

    #try:
    make_python(graphs, symanticName)
    #except Exception:
     #   print('error while creating python file')
      #  return 'error while creating python file', -1

    code_name = symanticName + '.py'
    try:
        dest_path = os.path.join('public/symanthic/', code_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copyfile(
            os.path.join(symanticName, code_name),
            dest_path)
    except Exception as m:
        print('error while copyfile' + str(m))
        return 'error while copyfile', -1

    return 'symanthic/' + code_name, 0
