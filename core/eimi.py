from helper import load_env_file
from optparse import OptionParser
from parser import syscall_parser
from qemu_manager import LibvirtHandler
from connection_handler import *
import os
from static_analyzer import Elf


def main():
    # Load .env file
    load_env_file()

    # Parse args and options
    parser = OptionParser("Usage: python3 eimi.py <sample_hash>")
    # parser.add_option('-t', dest='test', type='string', help="test option")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print("Usage: " + parser.usage)
        exit(1)

    if not os.path.isfile(args[0]):
        print(colored("[X] Sample file not found", 'red'))
        exit(1)

    if not os.access(args[0], os.R_OK):
        print(colored("[X] Access denied to local sample file", 'red'))
        exit(1)

    #######################
    ### Static analysis ###
    #######################
    sample = Elf(args[0])
    sample.information_file()

    if sample.bintype != 'elf':
        print(colored("[X] It is not a ELF sample", 'red'))
        exit(1)

    # Parse sample arch to deploy a virtual machine
    vm_guest = sample.arch + '_' + str(sample.bits) + '_' + sample.endian
    vm_path = '../machines/' + vm_guest

    # Check if virtual machine is imported in the project
    if not os.path.isdir(vm_path):
        print(colored("[X] Virtual machine not found", 'red'))
        exit(1)

    if not os.path.isfile(vm_path + '/' + vm_guest + '.xml'):
        print(colored("[X] Virtual machine XML schema not found", 'red'))
        exit(1)

    '''
    sample.sections_file()
    sample.imports_file()
    sample.libs_file()
    sample.hash_file()
    sample.get_strings()
    sample.get_opcodes_func()
    sample.get_ngrams()
    sample.get_cyclomatic_complexity()
    '''

    ################################
    ### Handling virtual machine ###
    ################################
    handler = LibvirtHandler()
    domain = handler.start_guest(vm_guest)

    ######################
    ### SSH connection ###
    ######################
    ssh = ssh_connect(os.getenv('MACHINE_IP'), int(os.getenv('MACHINE_PORT')), os.getenv('SSH_USER'),
                      os.getenv('SSH_PASSWORD'))

    if ssh is None:
        handler.stop_guest(domain)  # Destroy virtual machine
        handler.shutdown()  # Close connection to qemu:///session
        exit(1)

    ########################
    ### Sample execution ###
    ########################
    run_sample(ssh, args[0], os.getenv('MACHINE_REMOTEPATH'))

    handler.stop_guest(domain)  # Destroy virtual machine
    handler.shutdown()  # Close connection to qemu:///session

    ########################
    ### Dynamic analysis ###
    ########################
    sysc = syscall_parser("tmp/"+hash+"/")

if __name__ == '__main__':
    main()
