import paramiko
import socket
from termcolor import colored
import os

CONNECTION_TIMEOUT = 3
EXECUTION_TIMEOUT = 3


def is_connection_successful(ip, port):
    socket.setdefaulttimeout(CONNECTION_TIMEOUT)
    sock = socket.socket()

    success = True

    try:
        sock.connect((ip, port))
    except socket.timeout:
        print(colored("[X] Connection timeout, virtual machine not found", 'red'))
        success = False
    except ConnectionRefusedError:
        print(colored("[X] Connection refused, closed port", 'red'))
        success = False
    except:
        print(colored("[X] Invalid IP or port format", 'red'))
        success = False
    finally:
        sock.close()

    return success


def ssh_connect(ip, port, username, password):
    ssh = paramiko.SSHClient()

    # Set unknown hosts policy (host key is not in known hosts file)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if is_connection_successful(ip, port):
        try:
            ssh.connect(ip, port=port, username=username, password=password, allow_agent=False, look_for_keys=False)
        except paramiko.ssh_exception.AuthenticationException:
            print(colored("[X] SSH wrong credentials", 'red'))
            exit(0)

        return ssh

    else:
        return None


def run_sample(ssh, localpath, remotepath):
    if not os.path.isfile(localpath):
        print(colored("[X] Sample file not found", 'red'))
        exit(0)

    if not os.access(localpath, os.R_OK):
        print(colored("[X] Access denied to local sample file", 'red'))
        exit(0)

    # if not os.access(localpath, os.R_OK): TODO
    # print(colored("[X] Access denied to local sample file", 'red'))
    # exit(0)

    # Split dir and sample file
    dirname, filename = os.path.split(localpath)

    sftp = ssh.open_sftp()

    # Upload sample to virtual machine
    try:
        sftp.put(localpath, os.path.join(remotepath, filename))
    except PermissionError:
        print(colored("[X] Access denied to remote path", 'red'))
        exit(0)

    # Build strace command TODO
    command = "strace -ff -o " + filename + " cat " + filename

    # Run strace in virtual machine
    ssh.exec_command(command, timeout=EXECUTION_TIMEOUT)

    # Download strace output files TODO
    # sftp.get(os.path.join(remotepath, filename), localpath)

    sftp.close()
    ssh.close()


def main():
    ip = "127.0.0.1"
    port = 2222
    username = "root"
    password = "km11"

    # localpath = "/Users/swarley/Downloads/download.png"
    localpath = "passwords.txt"
    remotepath = "/home/msfadmin"

    ssh = ssh_connect(ip, port, username, password)

    run_sample(ssh, localpath, remotepath)


if __name__ == "__main__":
    main()
