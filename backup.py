from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import time
import datetime
import os
import glob
from time import gmtime, strftime
import logging
import threading
import schedule


localtime = time.localtime()
result = time.strftime("%d-%m-%Y_%H-%M", localtime)
zaman = time.strftime("%d-%m-%Y", localtime)
prefix_path = ("/Backup/")
file_array = [f for f in os.listdir(prefix_path) if f.endswith('.txt')]
file_array.sort()  # file is sorted list
file_array = [os.path.join(prefix_path, name) for name in file_array]

directory = str(zaman)
parent_dir = "/Error/"

path = os.path.join(parent_dir, directory)
os.mkdir(path)

for filename in file_array:
    log = open(filename, 'r')

for y in log:
    IP = y.rstrip("\n")
    print('\n  ' + IP.strip() + ' \n')
    RTR = {
        'ip':   IP,
        'device_type': '[Swicth]_ios',
        'username': '[Swicth_UserName]',
        'password': '[Swicth_Password]',
    }
    try:
        net_connect = ConnectHandler(**RTR)
    except NetMikoTimeoutException:
        Device_Not_Reach = print('Device not reachable.')
        z = "/Backup/Not_Reach_Backup/"
        t = str("Device_Not_Reach"+"_"+str(zaman)+".txt")
        device_not_reach_file = open(os.path.join(z, t), 'a')
        device_not_reach_file.write(IP+'\n')
        device_not_reach_file.close
        time.sleep(2)
        continue
    except AuthenticationException:
        Device_Not_Reach = print('Authentication Failure.')
        x = "/Backup/Not_Auth_Backup/"
        y = str("Device_Not_Auth"+"_"+str(zaman)+".txt")
        device_not_auth_file = open(os.path.join(x, y), 'a')
        device_not_auth_file.write(IP+'\n')
        device_not_auth_file.close
        time.sleep(2)
        continue
    except SSHException:
        Device_Success = print('Initiating config backup')
        p = "/Backup/Success Backup/"
        r = str("Device_Success"+"_"+str(zaman)+".txt")
        device_success_file = open(os.path.join(p, r), 'a')
        device_success_file.write(IP+'\n')
        device_success_file.close
        continue
    print('Initiating config backup')
    output = net_connect.send_command('show run')

    # Name of text file coerced with +.txt
    name = str('RTR_'+IP+'_'+str(result))
    SAVE_FILE = open(os.path.join(path, name), 'w')
    # SAVE_FILE = open("RTR_"+IP+'_'str(result), 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print('Finished config backup')
