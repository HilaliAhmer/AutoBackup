from colorama import just_fix_windows_console
from termcolor import colored
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.exceptions import AuthenticationException
from Controllers.path import Paths
from Controllers.smtpSettings import EmailConfig
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Controllers.smtpSettings import EmailConfig
import zipfile
import time
import os
import smtplib

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
            Paths.NOT_AUT_BACKUP_PATH())+'\\'+not_aut_time, 'a')
        device_not_aut_file.write(IP+' Authentication failure'+'\n')
        device_not_aut_file.close
        Device_Not_Aut = print(colored(IP+' adresi kurulmak istenen bağlantıda kullanıcı adı veya şifre doğru değil. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(
            device_not_aut_file.name), 'red', attrs=["bold"]))
        time.sleep(2)
        continue
    except NetMikoTimeoutException:
        not_reach_time = str("Device_Not_Reach"+"_"+str(zaman)+'_'+".txt")
        device_not_reach_file = open(os.path.join(
            Paths.NOT_REACH_BACKUP_PATH())+'\\'+not_reach_time, 'a')
        device_not_reach_file.write(IP+' Request timed out.'+'\n')
        device_not_reach_file.close
        Device_Not_Reach = print(colored(IP+' adresi ile bağlantı kurulurken, bağlantı zaman aşımına uğradı. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(
            device_not_reach_file.name), 'red', attrs=["bold"]))
        time.sleep(2)
        continue
    except SSHException:
        ssh_failure = str("Device_SSH_Failure"+"_"+str(zaman)+".txt")
        device_ssh_failure = open(os.path.join(
            Paths.SSH_FAILURE_PATH())+'\\'+ssh_failure, 'a')
        device_ssh_failure.write(IP+'\n')
        device_ssh_failure.close
        Device_Success = print(colored(IP+' adresi ile bağlantı kurulurken SSH2 protokolü anlaşmasındaki başarısızlıklar veya mantık hatalarından kaynaklanan istisna oluştu. Günlüğe kaydedildi. {0} dosyasında bulabilirsiniz.'.format(device_ssh_failure.name), 'red', attrs=["bold"]))
        continue
    output = net_connect.send_command('show running-config')
  
    #Backupları gün bazlı tuttuğumuz folderı oluşturuyoruz.
    ## folder var mı yok mu kontrol ediyoruz.
    folderName=str(zaman)
    if not os.path.exists(os.path.join(Paths.BACKUP_PATH(), folderName)):
        os.makedirs(os.path.join(Paths.BACKUP_PATH(), folderName))
        print(colored(folderName +' isminde bir backup oluşturuldu..', 'green', attrs=["bold"]))
    folderPath=os.path.join(Paths.BACKUP_PATH(), folderName)
    backupName = str(net_connect.base_prompt+' - '+IP+' - '+str(result)+".txt")
    SAVE_FILE = open(os.path.join(folderPath,backupName ), 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print(colored(IP +' - Backup başarı ile alındı..', 'green', attrs=["bold"]))

# Kaynak klasör ve hedef zip dosyasının yolları
zip_dosyasi_yolu = os.path.join(Paths.BACKUPZIP_PATH())
zip_dosyasi_yolu=zip_dosyasi_yolu+'\\'+zaman+'.zip'
# ZipFile nesnesini yazma modunda oluşturuyoruz. 
# Bu, belirttiğimiz yolda bir .zip dosyası oluşturacak.
with zipfile.ZipFile(zip_dosyasi_yolu, 'w') as zipf:
    # os.walk, belirttiğimiz klasör içindeki tüm klasörleri ve dosyaları dolaşmamıza olanak tanır.
    # Bu fonksiyon üçlü bir tuple döndürür: (klasör_adı, alt_klasorler, dosyalar)
    for foldername, subfolders, filenames in os.walk(os.path.join(Paths.BACKUP_PATH())):
        for filename in filenames:
            # Her dosya için tam yolunu oluşturuyoruz
            tam_dosya_yolu = os.path.join(foldername, filename)
            
            # os.path.relpath ile dosyanın sıkıştırılacak zip dosyası içerisindeki 
            # göreceli yolunu elde ediyoruz.
            # Bu sayede zip içerisinde orijinal klasör yapısını koruyabiliriz.
            zip_icerisindeki_dosya_yolu = os.path.relpath(tam_dosya_yolu, os.path.join(Paths.BACKUP_PATH()))
            
            # Dosyayı zip'e ekliyoruz.
            zipf.write(tam_dosya_yolu, zip_icerisindeki_dosya_yolu)
print(colored(f"'{zip_dosyasi_yolu}' olarak sıkıştırma tamamlandı.", 'green', attrs=["bold"]))         

# E-posta gönderme
mesaj = MIMEMultipart()
mesaj['From'] = EmailConfig.SENDER
mesaj['To'] = ', '.join(EmailConfig.RECEIVERS)
mesaj['Subject'] = EmailConfig.SUBJECT
mesaj.attach(MIMEText(EmailConfig.BODY, 'plain'))

with open(zip_dosyasi_yolu, 'rb') as file:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="SwitchBackup_'+folderName+'.zip"')
    mesaj.attach(part)
text = MIMEText('Merhaba, sıkıştırılmış dosyayı ekte bulabilirsiniz.')
mesaj.attach(text)
try:
    with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
        # TLS (güvenli bağlantı) kullanıyorsan aşağıdaki satırı etkinleştir.
        #server.starttls()
        #server.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
        server.sendmail(EmailConfig.SENDER, EmailConfig.RECEIVERS, mesaj.as_string())
    print(colored('E-posta başarıyla gönderildi!', 'green', attrs=["bold"]))
except Exception as e:
    print(colored("E-posta gönderilirken bir hata oluştu: {e}", 'red', attrs=["bold"]))