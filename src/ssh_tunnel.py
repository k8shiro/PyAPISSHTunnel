import paramiko
import time
# override reverse_forward_tunnel method
from rforward import handler #reverse_forward_tunnel
import threading
import json

REMOTE_SERVER = None
REMOTE_PORT = None 
SSH_USERNAME = None
SSH_PASSWORD = None
SSH_KEY_FILENAME = None

TUNNEL_SERVER_PORT = None
TUNNEL_REMOTE_HOST = None
TUNNEL_REMOTE_PORT = None
SSH_TIMEOUT = None

LOGIN_CHECK = False
LOGIN_CHECK_INTERVAL = None
# It is same as openssh -R option 
# "ssh -R TUNNEL_SERVER_PORT:TUNNEL_REMOTE_HOST:TUNNEL_REMOTE_PORT SSH_USERNAME@SSH_PASSWORD"


def update_ssh_settings():
    global REMOTE_SERVER 
    global REMOTE_PORT 
    global SSH_USERNAME 
    global SSH_PASSWORD 
    global SSH_KEY_FILENAME 
    
    global TUNNEL_SERVER_PORT 
    global TUNNEL_REMOTE_HOST 
    global TUNNEL_REMOTE_PORT 
    global SSH_TIMEOUT

    global LOGIN_CHECK 
    global LOGIN_CHECK_INTERVAL 

    with open('/config.json') as f:
        settings = jsn = json.load(f)
        ssh_settings = settings['SSH_SETTINGS']
        print(ssh_settings)
        REMOTE_SERVER = ssh_settings['REMOTE_SERVER']
        REMOTE_PORT = int(ssh_settings['REMOTE_PORT'])
        SSH_USERNAME = ssh_settings['SSH_USERNAME']
        SSH_PASSWORD = ssh_settings['SSH_PASSWORD'] if ssh_settings['SSH_PASSWORD'] else None
        SSH_KEY_FILENAME = '/key/' + ssh_settings['SSH_KEY_FILENAME'] if ssh_settings['SSH_KEY_FILENAME'] else None
        
        TUNNEL_SERVER_PORT = int(ssh_settings['TUNNEL_SERVER_PORT'])
        TUNNEL_REMOTE_HOST = ssh_settings['TUNNEL_REMOTE_HOST']
        TUNNEL_REMOTE_PORT = int(ssh_settings['TUNNEL_REMOTE_PORT'])
        SSH_TIMEOUT = int(ssh_settings['SSH_TIMEOUT'])

        login_check_settings = settings['LOGIN_CHECK_SETTINGS']
        LOGIN_CHECK = login_check_settings['LOGIN_CHECK']
        LOGIN_CHECK_INTERVAL = int(login_check_settings['LOGIN_CHECK_INTERVAL'])


def login_user_check():
    # 暫定対応
    import warnings
    warnings.filterwarnings(action='ignore',module='.*paramiko.*')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(REMOTE_SERVER, port=REMOTE_PORT, username=SSH_USERNAME, password=SSH_PASSWORD, key_filename=SSH_KEY_FILENAME)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('who -q')
    login_users = set(ssh_stdout.readline().split())
    if SSH_USERNAME in login_users:
        login_users.remove(SSH_USERNAME)

    if len(login_users) == 0:
        return False
    else:
        print("LOGIN USERS:{}".format(' '.join(login_users)))
        return True


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        chan = transport.accept(SSH_TIMEOUT)
        if chan is None:
            return True
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()


def create_ssh_tunnel():
    transport = paramiko.Transport((REMOTE_SERVER, REMOTE_PORT))
    if SSH_KEY_FILENAME:
        private_key = paramiko.RSAKey.from_private_key_file(SSH_KEY_FILENAME)
    transport.connect(hostkey  = None,
                  username = SSH_USERNAME,
                  password = SSH_PASSWORD,
                  pkey     = private_key)
    reverse_forward_tunnel(9876, '192.168.2.30', 8889, transport)
    transport.close()


def run_forwading():
    while True:
        if LOGIN_CHECK == True:
            exists_user = login_user_check()
            print("Check")
            if not exists_user:
              print("USER NOT LOGIN, SLEEP 10s")
              time.sleep(LOGIN_CHECK_INTERVAL)
              continue
    
        create_ssh_tunnel()


if __name__ == '__main__':
    update_ssh_settings()
    run_forwading()





