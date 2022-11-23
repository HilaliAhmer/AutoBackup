from colorama import just_fix_windows_console
from termcolor import colored
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.exceptions import AuthenticationException
from Controllers.path import Paths
import time
import os

just_fix_windows_console()
# loglama için zaman ayarı.
localtime = time.localtime()
result = time.strftime("%d-%m-%Y_%H-%M", localtime)
zaman = time.strftime("%d-%m-%Y", localtime)

dosya = open(Paths.INVENTORY_PATH(), "r")
for IP in dosya:
    if (IP[-1:] == '\n'):
        IP = IP.strip("\n")
    else:
        IP = IP
    SW = {
        'ip':   IP,
        'device_type': '[DEVICE_TYPE]',
        'username': '[SWITCH_USERNAME]',
        'password': '[SWITCH_PASSWORD]',
    }
    try:
        net_connect = ConnectHandler(**SW)
    except AuthenticationException:
        not_aut_time = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_aut_file = open(os.path.join(
            Paths.NOT_AUT_BACKUP_PATH())+'\\'+not_aut_time, 'w')
        device_not_aut_file.write(IP+'\n')
        device_not_aut_file.close
        Device_Not_Aut = print(colored('Kullanıcı adı veya şifre doğru değil. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(
            device_not_aut_file.name), 'red', attrs=["bold"]))
        time.sleep(2)
        continue
    except NetMikoTimeoutException:
        not_reach_time = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_reach_file = open(os.path.join(
            Paths.NOT_REACH_BACKUP_PATH())+'\\'+not_reach_time, 'w')
        device_not_reach_file.write(IP+'\n')
        device_not_reach_file.close
        Device_Not_Reach = print(colored('Bağlantı zaman aşımına uğradı. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(
            device_not_reach_file.name), 'red', attrs=["bold"]))
        time.sleep(2)
        continue
    except SSHException:
        ssh_failure = str("Device_SSH_Failure"+"_"+str(zaman)+".txt")
        device_ssh_failure = open(os.path.join(
            Paths.SSH_FAILURE_PATH())+'\\'+ssh_failure, 'w')
        device_ssh_failure.write(IP+'\n')
        device_ssh_failure.close
        Device_Success = print(colored(
            'SSH2 protokolü anlaşmasındaki başarısızlıklar veya mantık hatalarından kaynaklanan istisna oluştu. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(device_ssh_failure.name), 'red', attrs=["bold"]))
        continue
    output = net_connect.send_command('show run')

    host=output.splitlines()
    for h in host:
        if h.startswith("hostname")==True:
            hostname=""
            hostname=h[10:-1]
            break
    if not hostname:
        hostname="SUCCESS_"

    name = str(hostname+'_'+IP+'_'+str(result)+".txt")
    SAVE_FILE = open(os.path.join(Paths.BACKUP_PATH(), name), 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print(colored('Backup başarı ile alındı..', 'green', attrs=["bold"]))
