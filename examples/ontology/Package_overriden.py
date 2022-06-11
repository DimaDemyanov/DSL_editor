# That file was generated automatically with DSL editor
# The moment of generation: 05/06/2022 15:41:36
from interpreter.ClassContainer import ClassContainer
from interpreter.AttrContainer import AttrContainer
from interpreter.ActContainer import ActContainer
from interpreter.AggrContainer import AggrContainer
from interpreter.ArgContainer import ArgContainer
from interpreter.ResContainer import ResContainer
from interpreter.MArgContainer import MArgContainer
from interpreter.MResContainer import MResContainer
from interpreter.EnumContainer import EnumContainer

class Package:

    #VARS
    def __init__(self, package_container, file):
        self.exitPackageFlag = False
        self.class_ = ""
        self.__state__ = "entry"

        self.package_container = package_container
        self.file = file

    #INNER
    def __getTypes(self):
        return Types(self.package_container.types, self.file)

    def __preProcess(self):
        print('{', file=self.file, end='')
        print('\"name\": \"' + self.package_container.name + '\",', file=self.file, end='')

    def __postProcess(self):
        print('}', file=self.file, end='')

    def __processClasses(self):
        print(',', file=self.file, end='')
        List('class', self.package_container.classes, self.file).run()

    def __processEnums(self):
        print(',', file=self.file, end='')
        List('enum', self.package_container.enums, self.file).run()

    def __processRels(self):
        print(',', file=self.file, end='')
        List('rel', self.package_container.rels, self.file).run()

    # PROVIDED
    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry":
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process":
                if True:
                    self.__preProcess()
                    self.__state__ = "types_processing"
                    continue
            if self.__state__ == "types_processing":
                if True:
                    types = self.__getTypes()
                    self.__state__ = "types_retrieved"
                    continue
            if self.__state__ == "types_retrieved":
                if True:
                    types.process()
                    self.__state__ = "types_processed"
                    continue
            if self.__state__ == "types_processed":
                if True:
                    self.__processEnums()
                    self.__state__ = "enums_processed"
                    continue
            if self.__state__ == "enums_processed":
                if True:
                    self.__processClasses()
                    self.__state__ = "classes_processed"
                    continue
            if self.__state__ == "classes_processed":
                if True:
                    self.__processRels()
                    self.__state__ = "rels_processed"
                    continue
            if self.__state__ == "rels_processed":
                if True:
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process":
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue


class List:

    #VARS
    def __init__(self, name, list, file):
        self.elem = ""
        self.__state__ = "entry"

        self.name = name
        self.list = list
        self.file = file
        self.elem_iterator = iter(list)
        self.current_elem = next(self.elem_iterator, None)

    #INNER
    def __processElem(self):
        if isinstance(self.elem, str):
            print('\"' + self.elem + '\"', file=self.file, end='')

        if isinstance(self.elem, ClassContainer):
            Class(self.elem, self.file).run()

        if isinstance(self.elem, AttrContainer):
            Attr(self.elem, self.file).run()

        if isinstance(self.elem, ActContainer):
            Act(self.elem, self.file).run()

        if isinstance(self.elem, ArgContainer):
            Arg(self.elem, self.file).run()

        if isinstance(self.elem, ResContainer):
            Res(self.elem, self.file).run()

        if isinstance(self.elem, AggrContainer):
            Aggr(self.elem, self.file).run()

        if isinstance(self.elem, MArgContainer):
            MArg(self.elem, self.file).run()

        if isinstance(self.elem, MResContainer):
            MRes(self.elem, self.file).run()

        if isinstance(self.elem, EnumContainer):
            Enums(self.elem, self.file).run()

    def __nextElem(self):
        elem = self.current_elem
        self.current_elem = next(self.elem_iterator, None)
        return elem

    def __nextElemExists(self):
        return True if self.current_elem else False

    def __preProcess(self):
        print('\"' + self.name + '\": [', file=self.file, end='')

    def __postProcess(self):
        print(']', file=self.file, end='')

    def __separate(self):
        print(',', file=self.file, end='')

    #PROVIDED
    def process(self):
        # TODO: add implementation
        pass

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry":
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process":
                if True:
                    self.__preProcess()
                    self.__state__ = "pre_check"
                    continue
            if self.__state__ == "pre_check":
                if self.__nextElemExists():
                    self.__state__ = "start_processing"
                    continue
                self.__state__ = "post_process"
                continue
            if self.__state__ == "start_processing":
                if True:
                    self.elem = self.__nextElem()
                    self.__state__ = "elem_processing"
                    continue
            if self.__state__ == "elem_processing":
                if True:
                    self.__processElem()
                    self.__state__ = "separation_check"
                    continue
            if self.__state__ == "separation_check":
                if self.__nextElemExists():
                    self.__separate()
                    self.__state__ = "start_processing"
                    continue
                self.__state__ = "post_process"
                continue
            if self.__state__ == "post_process":
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue


class Types:

    #VARS
    def __init__(self, types_container, file):
        self.exitTypesFlag = False
        self.types = types_container.typeNames
        self.__state__ = "entry"

        self.types_container = types_container
        self.file = file

    #INNER
    def __processTypes(self):
        List('types', self.types, self.file).run()

    def __preProcess(self):
        pass

    def __postProcess(self):
        pass

    #PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process" :
                if True:
                    self.__preProcess()
                    self.__state__ = "start_processing"
                    continue
            if self.__state__ == "start_processing" :
                if True:
                    self.__processTypes()
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process" :
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue


class Enums:

    #VARS
    def __init__(self, container, file):
        self.enums = ""
        self.__state__ = "entry"

        self.container = container
        self.file = file

    #INNER
    def __processEnums(self):
        List('literals', self.container.constants, self.file).run()

    def __preProcess(self):
        print('{', file=self.file, end='')
        print('\"name\": \"' + self.container.name + '\",', file=self.file, end='')

    def __postProcess(self):
        print('}', file=self.file, end='')

    #PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process" :
                if True:
                    self.__preProcess()
                    self.__state__ = "start_processing"
                    continue
            if self.__state__ == "start_processing" :
                if True:
                    self.__processEnums()
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process" :
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue



class Class:

    #VARS
    def __init__(self, class_container, file):
        self.exitClassesFlag = False
        self.__state__ = "entry"

        self.class_container = class_container
        self.file = file

    #INNER
    #PROVIDED
    def __process(self):
        self.run()

    def __processAttrs(self):
        List('attr', self.class_container.attrs, self.file).run()

    def __processOpers(self):
        List('oper', self.class_container.opers, self.file).run()

    def __preProcess(self):
        print('{', file=self.file, end='')
        print('\"name\": \"' + self.class_container.name + '\",', file=self.file, end='')

    def __postProcess(self):
        print('}', file=self.file, end='')

    def __separate(self):
        print(',', file=self.file, end='')

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry":
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process":
                if True:
                    self.__preProcess()
                    self.__state__ = "attr_processing"
                    continue
            if self.__state__ == "attr_processing":
                if True:
                    self.__processAttrs()
                    self.__state__ = "separate"
                    continue
            if self.__state__ == "separate":
                if True:
                    self.__separate()
                    self.__state__ = "oper_processing"
                    continue
            if self.__state__ == "oper_processing":
                if True:
                    self.__processOpers()
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process":
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue

class Act:

    #VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    #INNER
    def __process(self):
        self.run()

    def __processArgs(self):
        List('arg', self.container.args, self.file).run()

    def __processRess(self):
        List('res', self.container.ress, self.file).run()

    def __preProcess(self):
        print('{', file=self.file, end='')
        print('\"type\": \"act\",', file=self.file, end='')
        print('\"name\": \"' + self.container.name + '\",', file=self.file, end='')

    def __postProcess(self):
        print('}', file=self.file, end='')

    def __separate(self):
        print(',', file=self.file, end='')

    #PROVIDED
    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process" :
                if True:
                    self.__preProcess()
                    self.__state__ = "args_processing"
                    continue
            if self.__state__ == "args_processing" :
                if True:
                    self.__processArgs()
                    self.__state__ = "separate"
                    continue
            if self.__state__ == "separate" :
                if True:
                    self.__separate()
                    self.__state__ = "ress_processing"
                    continue
            if self.__state__ == "ress_processing" :
                if True:
                    self.__processRess()
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process" :
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue


class Aggr:

    # VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    # INNER
    def __process(self):
        self.run()

    def __processMArgs(self):
        List('arg', self.container.m_args, self.file).run()

    def __processMRess(self):
        List('res', self.container.m_ress, self.file).run()

    def __preProcess(self):
        print('{', file=self.file, end='')
        print('\"type\": \"aggr\",', file=self.file, end='')
        print('\"name\": \"' + self.container.name + '\",', file=self.file, end='')

    def __postProcess(self):
        print('}', file=self.file, end='')

    def __separate(self):
        print(',', file=self.file, end='')

    #PROVIDED
    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "pre_process"
                    continue
            if self.__state__ == "pre_process" :
                if True:
                    self.__preProcess()
                    self.__state__ = "attr_processing"
                    continue
            if self.__state__ == "attr_processing" :
                if True:
                    self.__processMArgs()
                    self.__state__ = "separate"
                    continue
            if self.__state__ == "separate" :
                if True:
                    self.__separate()
                    self.__state__ = "oper_processing"
                    continue
            if self.__state__ == "oper_processing" :
                if True:
                    self.__processMRess()
                    self.__state__ = "post_process"
                    continue
            if self.__state__ == "post_process" :
                if True:
                    self.__postProcess()
                    self.__state__ = "exit"
                    continue


class Arg:

    # VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    # INNER
    def __process(self):
        name_ = '\"type\": \"' + self.container.type_name + '\", ' if self.container.type_name else ''
        print('{ ' + name_ + '\"name\": \"' + self.container.name + '\"}', file=self.file, end='')

    # PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "processing"
                    continue
            if self.__state__ == "processing" :
                if True:
                    self.__process()
                    self.__state__ = "exit"
                    continue


class Res:

    # VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    # INNER
    def __process(self):
        name_ = '\"type\": \"' + self.container.type_name + '\", ' if self.container.type_name else ''
        print('{ ' + name_ + '\"name\": \"' + self.container.name + '\"}', file=self.file, end='')

    # PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "processing"
                    continue
            if self.__state__ == "processing" :
                if True:
                    self.__process()
                    self.__state__ = "exit"
                    continue


class MArg:

    # VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    # INNER
    def __process(self):
        name_ = '\"type\": \"' + self.container.type_name + '\", ' if self.container.type_name else ''
        print('{ ' + name_ + '\"name\": \"' + self.container.name + '\"}', file=self.file, end='')

    # PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry":
                if True:
                    self.__state__ = "processing"
                    continue
            if self.__state__ == "processing":
                if True:
                    self.__process()
                    self.__state__ = "exit"
                    continue


class MRes:

    # VARS
    def __init__(self, container, file):
        self.__state__ = "entry"

        self.container = container
        self.file = file

    # INNER
    def __process(self):
        name_ = '\"type\": \"' + self.container.type_name + '\", ' if self.container.type_name else ''
        print('{ ' + name_ + '\"name\": \"' + self.container.name + '\"}', file=self.file, end='')

    # PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry":
                if True:
                    self.__state__ = "processing"
                    continue
            if self.__state__ == "processing":
                if True:
                    self.__process()
                    self.__state__ = "exit"
                    continue


class Attr:

    #VARS
    def __init__(self, attr_container, file):
        self.__state__ = "entry"

        self.attr_container = attr_container
        self.file = file

    #INNER
    def __process(self):
        name_ = '\"type\": \"' + self.attr_container.typeName + '\", ' if self.attr_container.typeName else ''
        print('{ ' + name_ + '\"name\": \"' + self.attr_container.name + '\"}', file=self.file, end='')

    #PROVIDED
    def process(self):
        self.run()

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if True:
                    self.__state__ = "processing"
                    continue
            if self.__state__ == "processing" :
                if True:
                    self.__process()
                    self.__state__ = "exit"
                    continue