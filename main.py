from colorama import Fore, Style
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.exceptions import AuthenticationException
import time
import os

#loglama için zaman ayarı.
localtime = time.localtime()
result = time.strftime("%d-%m-%Y_%H-%M", localtime)
zaman = time.strftime("%d-%m-%Y", localtime)

#Root Folder yapılandırası
ROOT_DIR = os.path.abspath(os.curdir)
BACKUP_PATH = os.path.join(ROOT_DIR, 'Backup')
ERROR_DIR = os.path.join(ROOT_DIR, 'Error')
INVENTORY_PATH = os.path.join(ROOT_DIR, 'InventoryList.txt')

#Error Folder Yapılandırması
Not_Aut_Backup = os.path.join(ROOT_DIR, 'Not_Aut_Backup')
Not_Reach_Backup = os.path.join(ROOT_DIR, 'Not_Reach_Backup')
SSH_Failure = os.path.join(ROOT_DIR, 'SSH_Failure')


dosya = open(INVENTORY_PATH, "r")
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
        device_not_aut_file = open(
            (os.path.join(Not_Aut_Backup))+not_aut_time, 'w')
        device_not_aut_file.write(IP+'\n')
        device_not_aut_file.close
        Device_Not_Aut = print(
            Fore.RED + 'Kullanıcı adı veya şifre doğru değil. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(device_not_aut_file.name))
        print(Style.RESET_ALL)
        time.sleep(2)
        continue
    except NetMikoTimeoutException:
        not_reach_time = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_reach_file = open(
            (os.path.join(Not_Reach_Backup))+not_reach_time, 'w')
        device_not_reach_file.write(IP+'\n')
        device_not_reach_file.close
        Device_Not_Reach = print(
            Fore.YELLOW+'Bağlantı zaman aşımına uğradı. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(device_not_reach_file.name))
        print(Style.RESET_ALL)
        time.sleep(2)
        continue
    except SSHException:
        ssh_failure = str("Device_SSH_Failure"+"_"+str(zaman)+".txt")
        device_ssh_failure = open(
            (os.path.join(SSH_Failure))+ssh_failure, 'w')
        device_ssh_failure.write(IP+'\n')
        device_ssh_failure.close
        Device_Success = print(
            Fore.GREEN+'SSH2 protokolü anlaşmasındaki başarısızlıklar veya mantık hatalarından kaynaklanan istisna oluştu. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(device_ssh_failure.name))
        print(Style.RESET_ALL)
        continue
    output = net_connect.send_command('show run')

    name = str('RTR_'+IP+'_'+str(result)+".txt")
    SAVE_FILE = open(os.path.join(BACKUP_PATH, name), 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print(Fore.GREEN +'Backup başarı ile alındı..')
    print(Style.RESET_ALL)