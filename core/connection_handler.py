import paramiko
import socket
from termcolor import colored
import os
import time
from scp import SCPClient, SCPException

CONNECTION_TIMEOUT = 30
DEPLOY_TIMEOUT = 10
EXECUTION_TIMEOUT = 20


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
    except Exception as e:
        print(colored(e, 'red'))
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
            time.sleep(DEPLOY_TIMEOUT)  # Timeout to deploy virtual machine and execute SSH service
            ssh.connect(ip, port=port, username=username, password=password, timeout=CONNECTION_TIMEOUT)
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

    # Create sample execution environment
    command = "cd " + remotepath + "; mkdir " + filename
    print(command)
    ssh.exec_command(command, timeout=EXECUTION_TIMEOUT)

    # Upload malware sample to virtual machine
    scp = SCPClient(ssh.get_transport())

    try:
        scp.put(localpath, remote_path=os.path.join(remotepath, filename))
    except SCPException as e:
        print(colored(e, 'red'))
        exit(0)

    # Build commands to execute in VM TODO
    command = "cd " + os.path.join(remotepath, filename) + "; strace -ff -o " + filename + " cat " + filename
    print(command)

    # Run strace in deployed virtual machine
    ssh.exec_command(command, timeout=EXECUTION_TIMEOUT)

    time.sleep(EXECUTION_TIMEOUT)  # Timeout to execute malware

    # Download strace output files
    scp.get(os.path.join(remotepath, filename), '../tmp', recursive=True)

    scp.close()
    ssh.close()
