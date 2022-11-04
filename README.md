# AutoBackup

Ortamınızda bulunan switchlerin otomatik backuplarını aldığı bir otomasyon sistemidir.

Kurulum:

pip install -r requirements.txt

main.py dosyasının içerisinde bulunan [DEVICE_TYPE] - [SWITCH_USERNAME] - [SWITCH_PASSWORD] alanlarını kendi yapınıza göre düzenlemeyi unutmayınız.

[DEVICE_TYPE] alanı için netmiko kütüphanesinin desteklediği devicelara DEVICE_TYPE.txt dosyasından ulaşabilirsiniz.

SW = {
        'ip':   IP,
        'device_type': '[DEVICE_TYPE]',
        'username': '[SWITCH_USERNAME]',
        'password': '[SWITCH_PASSWORD]',
    }


Backup başlatmak için:

python main.py