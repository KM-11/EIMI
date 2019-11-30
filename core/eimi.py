import os
from helper import load_env_file, store_static_fields
from optparse import OptionParser
from qemu_manager import LibvirtHandler
from connection_handler import *
from static_analyzer import Elf
from datetime import date
import json
from parser import syscall_parser
import glob
from cluster import *


def pipeline(sample_path, sample_name, options):
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

    print(colored("[+] Analyzing sample statically...", 'green'))

    # Radare2 static analysis fields
    sample.sections_file()
    sample.imports_file()
    sample.libs_file()
    sample.hash_file()
    # sample.get_strings()
    sample.get_opcodes_func()
    sample.get_ngrams()
    sample.get_cyclomatic_complexity()

    # Parse above fields into dictionary
    sample_info = json.dumps(sample.dump_to_dict())

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
        print(colored("[+] Destroying '" + vm_guest + "' virtual machine\n", 'green'))
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
    syscalls = syscall_parser("../tmp/" + sample_name)  # Dynamic data

    ########################
    ### Database queries ###
    ########################
    print(colored("[+] Storing analysis results into database", 'green'))
    db_fields = (sample.md5, sample_name, str(syscalls), None, None, vm_guest, sample_info, date.today())
    store_static_fields(db_fields)

    # End of pipeline

    cluster_ngrams(sample)
    print(colored("[+] Done!\n", 'green'))


def main():
    # Load .env file
    load_env_file()

    # Parse args and options
    parser = OptionParser("Usage: python3 eimi.py -r MODE <sample_hash>")

    parser.add_option('-d', '--directory', dest='samples_directory', type='string', default=None,
                      help="directory containing samples to execute")

    parser.add_option('-k', '--private-key', dest='private_key_file', type='string', default=None,
                      help="access virtual machine ssh service using private key")

    parser.add_option('-r', '--restrict-internet', dest='internet_access_mode', type='string', default='on',
                      help="restrict ('on') or permit ('off') virtual machines internet access")

    (options, args) = parser.parse_args()

    # Validate options and args
    if options.samples_directory is not None and not os.path.isdir(options.samples_directory):
        print(colored("[X] Samples directory not found", 'red'))
        exit(1)

    if options.private_key_file is not None and not os.path.isfile(options.private_key_file):
        print(colored("[X] SSH private key not found", 'red'))
        exit(1)

    if options.internet_access_mode not in ['on', 'off']:
        print("Usage: " + parser.usage)
        exit(1)

    if len(args) < 1:
        print("Usage: " + parser.usage)
        exit(1)

    # Multiple pipelines
    if options.samples_directory is None:  # Samples by args
        for arg in args:
            error = False

            if not os.path.isfile(arg):
                print(colored("[X] Sample file not found", 'red'))
                error = True

            if not os.access(arg, os.R_OK):
                print(colored("[X] Access denied to local sample file", 'red'))
                error = True

            # Execute pipeline
            if not error:
                # Split dir and sample file
                dirname, filename = os.path.split(arg)
                print(colored("[+] Sample: " + filename, 'blue'))

                pipeline(arg, filename, options)
    else:  # Samples in a directory
        samples_dir = glob.glob(options.samples_directory + "/*")

        for sample in samples_dir:
            error = False

            if not os.path.isfile(sample):
                print(colored("[X] Sample file not found", 'red'))
                error = True

            if not os.access(sample, os.R_OK):
                print(colored("[X] Access denied to local sample file", 'red'))
                error = True

            # Execute pipeline
            if not error:
                # Split dir and sample file
                dirname, filename = os.path.split(sample)
                print(colored("[+] Sample: " + filename, 'blue'))

                pipeline(sample, filename, options)


if __name__ == '__main__':
    main()
