from helper import load_env_file
from optparse import OptionParser
from qemu_manager import LibvirtHandler
from connection_handler import *


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

    # Handling Virtual machine
    handler = LibvirtHandler()
    domain = handler.start_guest('arm_32_little')  # TODO

    # SSH connection

    ssh = ssh_connect("localhost", 2222, "root", "km11")

    if ssh is None:
        handler.stop_guest(domain)  # Destroy virtual machine
        handler.shutdown()  # Close connection to qemu:///session
        exit(0)

    print(ssh)

    # Sample execution
    # run_sample(ssh, localpath, remotepath)

    handler.stop_guest(domain)  # Destroy virtual machine
    handler.shutdown()  # Close connection to qemu:///session

    # Dynamic analysis


if __name__ == '__main__':
    main()
