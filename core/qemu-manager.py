import libvirt 
import os 



def get_xml(arch):
	file = 'machines/'+arch+'/'+arch+'.xml'
	print(file)
	if os.path.isfile(file):
		with open(file,'r') as f:
			xml = f.read()
		return xml
	else:
		return None

def convert_rel_to_abs(arch):
	path_dir = 'machines/' + arch
	if os.path.isdir(path_dir):
		return os.path.abspath(path_dir) + '/'
	else:
		return None 

class  LibvirtHandler:

	def __init__(self):
		self.conn = libvirt.open('qemu:///session')
		if self.conn == None:
			print("No se ha podido conectar a qemu:///session")
			exit(1)


	def start_guest(self,arch):
		xml = get_xml(arch)
		if xml is None:
			print("El archivo xml no existe")
			return None
		abs_path = convert_rel_to_abs(arch)
		if abs_path is None:
			print("No existe la arquitectura indicada")
			return None
		

		path_kernel = abs_path
		path_file_system=abs_name
		path_dtb=abs_name

		xml_formated = xml.format(path_kernel=path_kernel,
								  path_dtb=path_dtb,
								  path_file_system=path_file_system)
		print(xml_formated)
		domain = self.conn.createXML(xml_formated)
		return domain

	def stop_guest(self,domain):
		domain.destroy()

	def shutdown(self):
		self.conn.close()




def main():
    a = LibvirtHandler()
	a.start_guest("ARM_32_LITTLE")


if __name__ == '__main__':
    main()