import os
import re
import shutil
import subprocess
from sys import platform as _platform
from datetime import datetime

from graphviz import Source


ANTLR_LAUNCH = 'antlr4'
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


def createFiles(source, syntax, grammarName):
    if not os.path.exists(grammarName):
        os.mkdir(grammarName)
    with open(os.path.join(grammarName, grammarName + '.g4'), 'w') as temp_file:
        temp_file.write(syntax)
    with open(os.path.join(grammarName, 'program'), 'w') as temp_file:
        temp_file.write(source)


def makeTemplate(grammarName, firstNode):
    shutil.copyfile(
        os.path.join('tree', 'template.py'),
        os.path.join(grammarName, 'interpreter.py'))
    s = open(os.path.join(grammarName, 'interpreter.py')).read()
    s = s.replace('(grammarName)', grammarName)
    s = s.replace('(firstNode)', firstNode)
    # add comments about automatic generation
    s = "# That file was generated automatically with DSL editor\n" + \
        f"# The moment of generation: {datetime.now().strftime(DATETIME_FORMAT)}\n\n\n" + s
    with open(os.path.join(grammarName, 'interpreter.py'), 'w') as f:
        f.write(s)


def buildGrammar(source, syntax):
    print('Getting grammar name and the first token')

    try:
        (grammarName, firstNode) = findNameAndStartToken(syntax)
    except Exception as m:
        print(m)
        print('file format error')
        return 'file format error', -1, None

    print('Saving source and syntax')
    try:
        createFiles(source, syntax, grammarName)
    except Exception as m:
        print(m)
        print('file system error')
        return 'file system error', -1, None

    print('Processing syntax with ANTLR')
    try:
        subprocess.call([ANTLR_LAUNCH, '-Dlanguage=Python3', '-o', grammarName, grammarName + '/' + grammarName + '.g4'], shell=IS_WINDOWS)
    except Exception as m:
        print(m)
        print('antlr error')
        return 'antlr error', -1, None

    return grammarName, 0, firstNode


def buildAST(source, syntax):
    grammarName, rc, firstNode = buildGrammar(source, syntax)
    if rc == -1:
        return grammarName, rc
    try:
        makeTemplate(grammarName, firstNode)
        subprocess.check_output([PYTHON_LAUNCH, 'interpreter.py', 'program'], stderr=subprocess.STDOUT,
                                    cwd=grammarName)
        print("Subprocess check_output finished ")
    except Exception as m:
        print(m)
        regex = r"(^Exception: line .*$)"
        s = re.findall(regex, m.output.decode('utf-8'), re.MULTILINE | re.IGNORECASE)
        return (s[0], -1) if len(s) > 0 else ("error while parse syntax", 1)
    try:
        graph = Source.from_file(os.path.join(grammarName, grammarName + '.dot'))
        graph.render(filename=grammarName, directory=grammarName, format='svg')  # raises exception

        svg_picture_name = 'AST/' + grammarName + '.svg'

        dest_path = os.path.join('public/', svg_picture_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copyfile(
            os.path.join(grammarName, grammarName + '.svg'),
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
        print("Cannot make template.py")
        print(m)
        return "Cannot make template.py", -1
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
