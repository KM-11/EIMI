import libvirt
import os
from termcolor import colored
import platform
from helper import load_env_file


def get_xml(arch):
    file = '../machines/' + arch + '/' + arch + '.xml'

    if os.path.isfile(file):
        with open(file, 'r') as f:
            xml = f.read()
        return xml
    else:
        return None


def convert_rel_to_abs(arch):
    path_dir = '../machines/' + arch

    if os.path.isdir(path_dir):
        return os.path.abspath(path_dir) + '/'
    else:
        return None


class LibvirtHandler:

    def __init__(self):
        self.conn = libvirt.open('qemu:///session')

        if self.conn is None:
            print(colored("[X] Could not connect to qemu:///session", 'red'))
            exit(1)

    def start_guest(self, arch):
        xml = get_xml(arch)

        if xml is None:
            print(colored("[X] XML file not found", 'red'))
            exit(1)

        abs_path = convert_rel_to_abs(arch)

        if abs_path is None:
            print(colored("[X] Indicated architecture does not exist", 'red'))
            exit(1)

        # Load .env file
        load_env_file()

        # Get system/OS name
        if platform.system() == 'Darwin':
            path_qemu = os.getenv('QEMU_MAC_PATH')
        else:
            path_qemu = os.getenv('QEMU_LINUX_PATH')

        xml_formatted = xml.format(machine_path=abs_path,
                                   path_qemu=path_qemu)

        domain = self.conn.createXML(xml_formatted)

        return domain

    def stop_guest(self, domain):
        domain.destroy()

    def shutdown(self):
        self.conn.close()
