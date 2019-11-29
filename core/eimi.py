from helper import load_env_file
from optparse import OptionParser
from qemu_manager import LibvirtHandler
from connection_handler import *
import os


def main():
    # Load .env file
    load_env_file()

    # Parse args and options
    parser = OptionParser("Usage: python3 eimi.py <sample_hash>")
    parser.add_option('-t', dest='test', type='string', help="test option")
    (options, args) = parser.parse_args()

    # if options.test is None or len(args) != 1:
    #   print("Usage: " + parser.usage)
    #   exit(0)

    # Static analysis
    #
    sample = Elf(file)
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
    sample.get_opcodes_func()
    sample.get_ngrams()
    sample.get_cyclomatic_complexity()
    # Handling virtual machine
    handler = LibvirtHandler()
    domain = handler.start_guest('arm_32_little')  # TODO

    # SSH connection
    ssh = ssh_connect(os.getenv('MACHINE_IP'), int(os.getenv('MACHINE_PORT')), os.getenv('SSH_USER'),
                      os.getenv('SSH_PASSWORD'))

    if ssh is None:
        handler.stop_guest(domain)  # Destroy virtual machine
        handler.shutdown()  # Close connection to qemu:///session
        exit(0)

    print(ssh)

    # Sample execution
    localpath = "../requirements.txt"
    remotepath = "/tmp"
    run_sample(ssh, localpath, remotepath)

    handler.stop_guest(domain)  # Destroy virtual machine
    handler.shutdown()  # Close connection to qemu:///session

    # Dynamic analysis
    #


if __name__ == '__main__':
    main()
