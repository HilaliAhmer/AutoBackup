# AutoBackup

An automation system that takes automatic backups of the switches in your environment.

## 🛠 Installation

```bash
pip install -r requirements.txt
```

Update the fields `[DEVICE_TYPE]`, `[SWITCH_USERNAME]`, and `[SWITCH_PASSWORD]` in the `main.py` file according to your own setup.

You can find the supported devices for `[DEVICE_TYPE]` in the `DEVICE_TYPE.txt` file, based on the devices supported by the Netmiko library.

```python
SW = {
    'ip':   IP,
    'device_type': '[DEVICE_TYPE]',
    'username': '[SWITCH_USERNAME]',
    'password': '[SWITCH_PASSWORD]',
}
```

## ▶️ Start Backup

```bash
python main.py
```

## 📧 Email Add-on (28.08.2023)

To enable email notifications after each backup, fill in your SMTP server details in `Controllers/smtpSettings.py`.  
Once configured, the system can automatically send a backup email to you after completion.
