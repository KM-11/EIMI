import r2pipe
import json
import base64

from nltk import ngrams


def get_ngrams(opcodes, n_ngram):
    return ngrams(opcodes, n_ngram)


class StaticAnalysis():
    def __init__(self, file):
        self.r2_handler = r2pipe.open(file)

    def __del__(self):
        self.r2_handler.quit()

    def get_info_file(self):
        return json.loads(self.r2_handler.cmd('ij'))

    def get_sections(self):
        sections = json.loads(self.r2_handler.cmd('iSj entropy'))['sections']
        sections_array = []
        for section in sections:

            section_dic = {}
            if 'name' in section:
                section_dic['name'] = section['name']

            if 'entropy' in section:
                section_dic['entropy'] = section['entropy']
            if 'perm' in section:
                section_dic['perm'] = section['perm']
            if 'size' in section:
                section_dic['size'] = section['size']

            sections_array.append(section_dic)
        return sections_array

    def get_imports(self):
        imports = json.loads(self.r2_handler.cmd('iij'))
        func_name_imp = list(map(lambda x: x['name'], imports))
        return func_name_imp

    def get_libs(self):
        libs = json.loads(self.r2_handler.cmd('ilj'))
        return libs

    def get_hash_file(self):
        hashes = json.loads(self.r2_handler.cmd('itj'))
        return hashes

    def get_data_strings(self):
        strings = json.loads(self.r2_handler.cmd('izj'))
        return list(map(lambda x: base64.b64decode(x['string']), strings))

    def get_list_func(self):
        self.r2_handler.cmd('aaa')
        func_list = json.loads(self.r2_handler.cmd('aflj'))

        func_list = list(map(lambda x: x['name'], func_list))

        return func_list

    def get_opcodes_func(self):

        func_list = self.get_list_func()
        func_opcodes = {}
        for func in func_list:
            if 'imp' not in func:
                opcodes = json.loads(self.r2_handler.cmd('s ' + func + "; pdfj"))
                opcodes = list(filter(lambda x: 'opcode' in x, opcodes['ops']))
                opcodes = list(map(lambda x: x['opcode'].split(' ')[0], opcodes))
                func_opcodes[func] = opcodes
        return func_opcodes

    def get_complexity_cyclomatic(self):
        func_list = self.get_list_func()
        func_cc = {}
        for func in func_list:
            if 'imp' not in func:
                func_cc[func] = json.loads(self.r2_handler.cmd('s ' + func + "; afCc"))

        print(func_cc)


class Elf:

    def __init__(self, file):
        self.static_analysis = StaticAnalysis(file)
        self.arch = None
        self.machine = None
        self.bits = None
        self.bintype = None
        self.compiler = None
        self.stripped = None
        self.endian = None
        self.sections = None
        self.imports = None
        self.libs = None
        self.md5 = None
        self.sha1 = None
        self.cc = None
        self.opcodes_func = None
        self.n_grams = None

    def information_file(self):
        binary_info = self.static_analysis.get_info_file()
        if 'bin' not in binary_info:
            print("No es un archivo EXECutable!!!!")
            exit(1)

        self.arch = binary_info['bin']['arch']
        self.machine = binary_info['bin']['machine']
        self.bits = binary_info['bin']['bits']
        self.bintype = binary_info['bin']['bintype']
        self.compiler = binary_info['bin']['compiler']
        self.stripped = binary_info['bin']['stripped']
        self.endian = binary_info['bin']['endian']

    def sections_file(self):
        self.sections = self.static_analysis.get_sections()

    def imports_file(self):
        self.imports = self.static_analysis.get_imports()

    def libs_file(self):
        self.libs = self.static_analysis.get_libs()

    def hash_file(self):
        hashes = self.static_analysis.get_hash_file()

        self.md5 = hashes['md5']
        self.sha1 = hashes['sha1']

    def get_cyclomatic_complexity(self):
        self.cc = self.static_analysis.get_complexity_cyclomatic()

    def get_opcodes_func(self):
        self.opcodes_func = self.static_analysis.get_opcodes_func()

    def get_ngrams(self):
        self.n_grams = []
        for func in self.opcodes_func:
            self.n_grams.extend(list(get_ngrams(self.opcodes_func[func], 6)))

    def stadistical_bb(self):
        pass

    def get_strings(self):
        self.strings = self.static_analysis.get_data_strings()

    def dump_to_dict(self):
        elf_dict = dict()
        elf_dict['arch'] = self.arch 
        elf_dict['machine'] = self.machine
        elf_dict['bits'] = self.bits
        elf_dict['bintype'] = self.bintype
        elf_dict['compiler'] = self.compiler
        elf_dict['stripped'] = self.stripped
        elf_dict['endian'] = self.endian
        elf_dict['sections'] = self.sections
        elf_dict['imports'] = self.imports
        elf_dict['libs'] = self.libs
        elf_dict['md5'] = self.md5
        elf_dict['sha1'] = self.sha1
        elf_dict['cc'] = self.cc
        elf_dict['opcodes_func'] = self.opcodes_func
        elf_dict['n_grams'] = self.n_grams
        return elf_dict