from helper import load_env_file, add_to_muestra
from optparse import OptionParser
from qemu_manager import LibvirtHandler
from connection_handler import *
import os
from static_analyzer import Elf
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from web.models import Muestra
import json



def pipeline(sample_path, options):
    #######################
    ### Static analysis ###
    #######################
    sample = Elf(sample_path)
    sample.information_file()

    if sample.bintype != 'elf':
        print(colored("[X] It is not a ELF sample", 'red'))
        return

    # Parse sample arch to deploy a virtual machine
    vm_guest = sample.arch + '_' + str(sample.bits) + '_' + sample.endian
    vm_path = '../machines/' + vm_guest

    # Check if virtual machine is imported in the project
    if not os.path.isdir(vm_path):
        print(colored("[X] Virtual machine not found", 'red'))
        return

    if not os.path.isfile(vm_path + '/' + vm_guest + '.xml'):
        print(colored("[X] Virtual machine XML schema not found", 'red'))
        return

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
    print(colored("[+] Starting '" + vm_guest + "' virtual machine...", 'green'))
    domain = handler.start_guest(vm_guest, options.internet_access_mode)

    # For security
    if domain is None:
        return

    ######################
    ### SSH connection ###
    ######################
    ssh = ssh_connect(os.getenv('MACHINE_IP'), int(os.getenv('MACHINE_PORT')), os.getenv('SSH_USER'),
                      os.getenv('SSH_PASSWORD'), options.private_key_file)

    if ssh is None:
        print(colored("[+] Shutting down '" + vm_guest + "' virtual machine", 'green'))
        handler.stop_guest(domain)  # Destroy virtual machine
        handler.shutdown()  # Close connection to qemu:///session
        return

    ########################
    ### Sample execution ###
    ########################
    run_sample(ssh, sample_path, os.getenv('MACHINE_REMOTEPATH'))

    print(colored("[+] Destroying '" + vm_guest + "' virtual machine", 'green'))
    handler.stop_guest(domain)  # Destroy virtual machine
    handler.shutdown()  # Close connection to qemu:///session

    ########################
    ### Dynamic analysis ###
    ########################
    # sysc = syscall_parser("tmp/" + hash + "/")
    print(colored("[+] Done!\n", 'green'))


def main():
    # Load .env file
    load_env_file()

    # Parse args and options
    parser = OptionParser("Usage: python3 eimi.py -r MODE -s MODE <sample_hash>")
    parser.add_option('-k', '--private-key', dest='private_key_file', type='string', default=None,
                      help="access virtual machine ssh service using private key")

    parser.add_option('-r', '--restrict-internet', dest='internet_access_mode', type='string', default='on',
                      help="restrict ('on') or permit ('off') virtual machines internet access")

    (options, args) = parser.parse_args()

    # Validate options and args
    if options.private_key_file is not None and not os.path.isfile(options.private_key_file):
        print(colored("[X] SSH private key not found", 'red'))
        exit(1)

    if options.internet_access_mode not in ['on', 'off']:
        print("Usage: " + parser.usage)
        exit(1)

    if len(args) < 1:
        print("Usage: " + parser.usage)
        exit(1)

    # Concurrent pipelines
    for arg in args:
        error = False

        if not os.path.isfile(arg):
            print(colored("[X] Sample file not found", 'red'))
            error = True

        if not os.access(arg, os.R_OK):
            print(colored("[X] Access denied to local sample file", 'red'))
            error = True

        # Split dir and sample file
        dirname, filename = os.path.split(arg)
        print(colored("[+] Analyzing sample: " + filename, 'blue'))

        # Execute pipeline
        if not error:
            pipeline(arg, options)

    ########################
    ###   Sample to db   ###
    ########################
    sample_info=str(sample.dump_todict())
    #sample_info = sample_info.replace("'", "\"")
    dynamic_info = {"syscalls":sysc}
    dynamic_info=str(dynamic_info)

    # ("hash", "nombre", "dinamico", None, None, "Arquitectura", "estatico", date.today())
    to_db=(sample.md5,None,dynamic_info,None,None,sample_info,date.today())
    helper.add_to_muestra(to_db)
    #dynamic_info=str(dynamic_info).replace("'", "\"")
    #sample_info = json.loads(sample_info)
    #dynamic_info=json.loads(dynamic_info)



if __name__ == '__main__':
    main()
