import r2pipe
import json
import base64

class StaticAnalysis():
	def __init__(self,file):
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
		func_name_imp = list(map(lambda x: x['name'],imports))
		return func_name_imp
		
	def get_libs(self):
		libs = json.loads(self.r2_handler.cmd('ilj'))
		return libs 

	def get_hash_file(self):
		hashes = json.loads(self.r2_handler.cmd('itj'))
		return hashes 
	def get_data_strings(self):
		strings = json.loads(self.r2_handler.cmd('izj'))
		return list(map(lambda x: base64.b64decode(x['string']),strings))
class elf:

	def __init__(self,file):
		self.static_analysis = StaticAnalysis(file)

	def information_file(self):
		binary_info = self.static_analysis.get_info_file()	
		if 'bin' not in binary_info:
			print("No es un archivo EXECutable!!!!")
			exit(1)

		self.arch = binary_info['bin']['arch']
		self.machine = binary_info['bin']['machine']
		self.bits = binary_info['bin']['bits']
		self.bintype = binary_info['bin']['bintype']
		self.compiler  = binary_info['bin']['compiler']
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
		pass
	def get_opcodes_func(self):
		pass 
	def stadistical_bb(self):
		pass
	def get_strings(self):
		self.strings = self.static_analysis.get_data_strings()
		
		
def main():
	file = 'PATH_PRUEBA_RAPIDA'
	sample = elf(file)
	sample.information_file()
	if sample.bintype != 'elf':
		print("No es un archivo ELF")
		exit(1)


	######PARA ELEGIR MAQUINA PARA EL DINAMICO##########

	print(sample.arch)
	print(sample.endian)
	print(sample.bits)

	sample.sections_file()
	sample.imports_file()
	sample.libs_file()
	sample.hash_file()
	sample.get_strings()
	
if __name__ == '__main__':
    main()

	


	








