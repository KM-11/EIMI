import paramiko
import socket
from termcolor import colored
import os
import time
from scp import SCPClient, SCPException
from helper import load_env_file


def is_connection_successful(ip, port):
    # Load .env file
    load_env_file()

    socket.setdefaulttimeout(int(os.getenv('CONNECTION_TIMEOUT')))
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


def ssh_connect(ip, port, username, password, private_key):
    # Load .env file
    load_env_file()

    ssh = paramiko.SSHClient()

    # Set unknown hosts policy (host key is not in known hosts file)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if is_connection_successful(ip, port):
        try:
            time.sleep(int(os.getenv('DEPLOY_TIMEOUT')))  # Timeout to deploy virtual machine and execute SSH service

            print(colored("[+] Connecting to virtual machine via SSH", 'green'))

            if private_key is None:
                # User and password login
                ssh.connect(ip, port=port, username=username, password=password,
                            timeout=int(os.getenv('CONNECTION_TIMEOUT')))
            else:
                # Private key login
                ssh.connect(ip, port=port, username=username, key_filename=private_key,
                            timeout=int(os.getenv('CONNECTION_TIMEOUT')))
        except paramiko.ssh_exception.AuthenticationException:
            print(colored("[X] SSH wrong credentials", 'red'))
            return None

        except paramiko.ssh_exception.SSHException as e:
            print(colored('[X] ' + str(e).capitalize(), 'red'))
            return None

        return ssh

    else:
        return None


def run_sample(ssh, localpath, remotepath):
    # Load .env file
    load_env_file()

    # Split dir and sample file
    dirname, filename = os.path.split(localpath)

    # Create sample execution environment
    command = "cd " + remotepath + "; mkdir " + filename
    ssh.exec_command(command)

    # Upload malware sample to virtual machine
    scp = SCPClient(ssh.get_transport())
    print(colored("[+] Uploading sample to virtual machine", 'green'))
    scp.put(localpath, remote_path=os.path.join(remotepath, filename))

    # Build commands to execute in VM
    command = "cd " + os.path.join(remotepath, filename) + "; chmod +x " + filename + "; strace -ff -o " \
              + filename + " ./" + filename + ' & sleep ' + os.getenv('EXECUTION_TIMEOUT') + "; kill -9 $!"

    # Run strace in deployed virtual machine
    ssh.exec_command(command)

    print(colored("[+] Executing sample (" + os.getenv('EXECUTION_TIMEOUT') + " secs)...", 'green'))
    time.sleep(int(os.getenv('EXECUTION_TIMEOUT')))  # Timeout to execute malware

    # Download strace output files
    if not os.path.isdir('../tmp'):
        os.mkdir('../tmp')

    print(colored(
        "[+] Downloading sample execution results in " + os.path.dirname(
            os.path.abspath('../' + __file__)) + '/tmp/' + filename, 'green'))
    scp.get(os.path.join(remotepath, filename), '../tmp', recursive=True)

    scp.close()
    ssh.close()
