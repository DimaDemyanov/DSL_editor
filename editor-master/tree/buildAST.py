import os
import re
import shutil
import subprocess
from datetime import datetime
from sys import platform as _platform

from graphviz import Source

ANTLR_LAUNCH = 'antlr4'
RRD_LAUNCH = 'rrd'
if _platform == "win32" or _platform == "win64":
    PYTHON_LAUNCH = 'python'
    # On Windows, ANTLR should be launched with subprocess with shell=True argument
    # On Linux, shell=False
    IS_WINDOWS = True
else:
    # It works on Ubuntu 20, You may change PYTHON_LAUNCH to suit the Python interpreter of Your system
    PYTHON_LAUNCH = 'python3'
    IS_WINDOWS = False

DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def findNameAndStartToken(syntax):
    regex = r"grammar\s+([A-Z][A-Z0-9_]*)\s*;[\n\s]*([A-Z][A-Z0-9_]*)"
    search = re.search(regex, syntax, re.MULTILINE | re.IGNORECASE)
    return (search.group(1), search.group(2))


def findFirstNode(syntax):
    words = syntax.split(' ')
    ind = -1
    for i, s in enumerate(words):
        if ':' in s:
            ind = i
            break
    if words[ind] == ':':  # node : symbol
        return words[ind - 1]
    if words[ind].startswith(':'):  # node :symbol
        return words[ind - 1]
    if words[ind].endswith(':'):  # node: symbol
        return words[ind].rstrip(':')
    if ':' in words[ind]:  # node:symbol
        end = words[ind].find(':')
        return words[ind][:end]


def createFiles(source, syntax, grammarName, dir):
    grammar_dir = os.path.join(dir, grammarName)
    if not os.path.exists(grammar_dir):
        os.mkdir(grammar_dir)
    with open(os.path.join(grammar_dir, grammarName + '.g4'), 'wb') as temp_file:
        temp_file.write(syntax.encode('UTF-8'))
    if source:
        with open(os.path.join(grammar_dir, 'program'), 'wb') as temp_file:
            temp_file.write(source.encode('UTF-8'))


def makeTemplate(grammarName, firstNode, dir):
    shutil.copyfile(
        os.path.join('tree', 'interpreter_template.py'),
        os.path.join(dir, grammarName, 'interpreter.py'))
    s = open(os.path.join(dir, grammarName, 'interpreter.py')).read()
    s = s.replace('(grammarName)', grammarName)
    s = s.replace('(firstNode)', firstNode)
    # add comments about automatic generation
    s = "# That file was generated automatically with DSL editor\n" + \
        f"# The moment of generation: {datetime.now().strftime(DATETIME_FORMAT)}\n\n\n" + s
    with open(os.path.join(dir, grammarName, 'interpreter.py'), 'w') as f:
        f.write(s)

# Tseytin Iteration: P#Q = (P Q)* P
# Often used for enumerations like (STRING COMMA)* STRING
def resolveTseytinIteration(syntax):
    new_syntax = ''

    for line_number, line in enumerate(syntax.splitlines()):
        line = line.replace('#', ' # ')
        words = line.split()
        new_words = []
        skipNext = False
        for i, _ in enumerate(words):
            if skipNext:
                skipNext = False
                continue
            if (words[i] == '#'):
                if i == 0 or i == len(words) - 1:
                    raise Exception('Tseytin iteration cant be parsed at line: ' + line_number)
                new_words[i - 1] = '(' + words[i - 1]
                new_words.append(words[i + 1] + ')*')
                new_words.append(words[i - 1])
                skipNext = True
            else:
                new_words.append(words[i])

        new_line = ''
        for i, word in enumerate(new_words):
            new_line = new_line + word + ' '

        new_syntax = new_syntax + new_line + '\n'

    return new_syntax

def preProcess(source, syntax, dir, tseytinEnabled = True):
    print('Getting grammar name and the first token')

    try:
        syntax = resolveTseytinIteration(syntax)
    except Exception as m:
        print(m)
        print('file format error')
        return str(m.output), None

    try:
        (grammarName, firstNode) = findNameAndStartToken(syntax)
        print('Extracted grammarName: ' + grammarName + ', firstNode: ' + firstNode)
    except Exception as m:
        print(m)
        print('file format error')
        return 'file format error', None

    print('Saving source and syntax')
    try:
        createFiles(source, syntax, grammarName, dir)
    except Exception as m:
        print(m)
        print('file system error')
        return 'file system error', None

    return grammarName, firstNode


def buildGrammar(source, syntax, dir):
    (grammarName, firstNode) = preProcess(source, syntax, dir)

    print('Processing syntax with ANTLR for grammar: ' + grammarName)

    try:
        grammar_file_path = os.path.join(dir, grammarName, grammarName + '.g4')
        language = '-Dlanguage=Python3'
        antlr_args = [ANTLR_LAUNCH, language, grammar_file_path]

        subprocess.check_output(antlr_args, stderr=subprocess.STDOUT, shell=IS_WINDOWS)
    except Exception as m:
        print('ANTLR error: ' + str(m))
        return 'ANTLR error: ' + re.sub('.*g4:', '', str(m.output)).replace('\\r\\n', '\n'), -1, None

    print('Syntax with ANTLR is successfully processed for grammar: ' + grammarName)

    return grammarName, 0, firstNode


def buildSyntaxDiagram(syntax, dir):
    grammarName, firstNode = preProcess(None, syntax, dir)

    print('Generating syntax diagram for grammar: ' + grammarName)

    try:
        grammar_file_path = grammarName + '/' + grammarName + '.g4'
        os.makedirs(dir + '/public/' + grammarName, exist_ok=True)
        rrd_args = [RRD_LAUNCH, '--simple', '--out', dir + '/public/' + grammarName + '/' + grammarName + '.html', dir + '/' + grammar_file_path]

        subprocess.check_output(rrd_args, stderr=subprocess.STDOUT, shell=IS_WINDOWS)
    except Exception as m:
        print('Syntax diagram rendering error: ' + str(m))
        return 'Syntax diagram rendering error: ' + str(m.output), None

    print('Successfully generated syntax diagram for grammar: ' + grammarName)

    return grammarName + '/' + grammarName + '.html', 0

def buildAST(source, syntax, dir):
    grammarName, rc, firstNode = buildGrammar(source, syntax, dir)
    if rc == -1:
        return grammarName, rc
    try:
        makeTemplate(grammarName, firstNode, dir)
        subprocess.check_output([PYTHON_LAUNCH, 'interpreter.py', 'program'], stderr=subprocess.STDOUT,
                                cwd=dir + '/' + grammarName)
        print("Subprocess check_output finished ")
    except Exception as m:
        print(m)
        regex = r"(^Exception: line .*$)"
        s = re.findall(regex, m.output.decode('utf-8'), re.MULTILINE | re.IGNORECASE)
        return (s[0], -1) if len(s) > 0 else ("error while parse syntax", 1)
    try:
        graph = Source.from_file(os.path.join(dir + '/' + grammarName, grammarName + '.dot'))
        graph.render(filename=grammarName, directory=dir + '/' + grammarName, format='svg')  # raises exception

        svg_picture_name = 'AST/' + grammarName + '.svg'

        dest_path = os.path.join(dir + '/' +'public/', svg_picture_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copyfile(
            os.path.join(dir + '/' + grammarName, grammarName + '.svg'),
            dest_path)
    except Exception as m:
        print(m)
        print('error while creating png file')
        return 'error while creating png file', -1

    return svg_picture_name, 0


def getInterpreter(source, syntax):
    # This function creates and sends zip-archive with ANTLR artifacts and the interpreter
    # called interpreter.py
    grammarName, rc, firstNode = buildGrammar(source, syntax)
    if rc == -1:
        return grammarName, rc
    try:
        makeTemplate(grammarName, firstNode)
    except Exception as m:
        print("Cannot make interpreter_template.py")
        print(m)
        return "Cannot make interpreter_template.py", -1
    try:
        # the folder to be archived is "grammarName"
        archive_ext = 'zip'
        interpreter_archive_name = 'interpreter/' + grammarName + '.' + archive_ext

        target_path = os.path.join('public/', interpreter_archive_name)
        # need to create archive in editor-master or Flask can't find it
        shutil.make_archive(grammarName, archive_ext, grammarName)
        # NOTE: if archive_ext == 'gztar', should repair target name
        # (archive_ext is not '.tar.gz' in this case)
        sendable_archive_name = grammarName + '.' + archive_ext
        # copy archive to the front/public, too
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        shutil.copyfile(grammarName + '.' + archive_ext,
                        target_path)
    except Exception as m:
        print('error while creating archive')
        print(m)
        return 'error while creating archive', -1

    return interpreter_archive_name, 0
