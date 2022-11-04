from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.exceptions import AuthenticationException
import time
import os

localtime = time.localtime()
result = time.strftime("%d-%m-%Y_%H-%M", localtime)
zaman = time.strftime("%d-%m-%Y", localtime)
success_backup_dir = ("./Backup/")
dosya = open("./InventoryList.txt", "r")
for IP in dosya:
    SW = {
        'ip':   IP,
        'device_type': '[DEVICE_TYPE]',
        'username': '[SWITCH_USERNAME]',
        'password': '[SWITCH_PASSWORD]',
    }
    try:
        net_connect = ConnectHandler(**SW)
    except AuthenticationException:
        Device_Not_Aut = print('Kimlik doğrulaması onaylanmadı.')
        not_aut_path = "./Error/Not_Aut_Backup/"
        not_aut_time = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_aut_file = open(
            (os.path.join(not_aut_path))+not_aut_time, 'w')
        device_not_aut_file.write(IP+'\n')
        device_not_aut_file.close
        time.sleep(2)
        continue
    except NetMikoTimeoutException:
        Device_Not_Reach = print('Cihaza ulaşılamıyor.')
        not_reach_path = "./Error/Not_Reach_Backup/"
        not_reach_time = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_reach_file = open(
            (os.path.join(not_reach_path))+not_reach_time, 'w')
        device_not_reach_file.write(IP+'\n')
        device_not_reach_file.close
        time.sleep(2)
        continue
    except SSHException:
        Device_Success = print('Initiating config backup')
        success_path = "./Error/Success_Backup/"
        success_time = str("Device_Success"+"_"+str(zaman)+".txt")
        device_success_file = open(
            (os.path.join(success_path))+success_time, 'w')
        device_success_file.write(IP+'\n')
        device_success_file.close
        continue
    print('Initiating config backup')
    output = net_connect.send_command('show run')

    name = str('RTR_'+IP+'_'+str(result)+".txt")
    SAVE_FILE = open(os.path.join(success_backup_dir, name), 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print('Finished config backup')
