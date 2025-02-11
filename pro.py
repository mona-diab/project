import os
import shutil
import requests
import smtplib
from email.mime.text import MIMEText
from urllib.parse import urlparse, unquote

# طلب البيانات من المستخدم
file_url = input("Enter the file URL: ")
email_receiver = input("Enter your email: ")

# استخدام مسارات متوافقة مع جميع الأجهزة
USER_HOME = os.path.expanduser("~")
DOWNLOAD_PATH = os.path.join(USER_HOME, "Downloads", "files")
BACKUP_PATH = os.path.join(USER_HOME, "Downloads", "backup")

# التأكد من وجود المجلدات المطلوبة
os.makedirs(DOWNLOAD_PATH, exist_ok=True)
os.makedirs(BACKUP_PATH, exist_ok=True)

# ثابتات البريد الإلكتروني (يجب استخدام كلمة مرور التطبيق عند التعامل مع Gmail)
EMAIL_SENDER = 'monadiab283@gmail.com'
EMAIL_PASSWORD = "lnlq bcbk kxrp vdfv"

# استخراج اسم الملف بطريقة آمنة
parsed_url = urlparse(file_url)
file_name = os.path.basename(parsed_url.path)
file_name = unquote(file_name)  # فك تشفير الاسم إذا كان مشفرًا
if not file_name:
    file_name = "downloaded_file"  # اسم افتراضي في حالة عدم توفر اسم صحيح

downloaded_file = os.path.join(DOWNLOAD_PATH, file_name)

print(f"Downloading file: {file_name} ...")
response = requests.get(file_url)
if response.status_code == 200:
    with open(downloaded_file, "wb") as file:
        file.write(response.content)
    print(f"Download succeeded: {downloaded_file}")
else:
    print("Download failed!")
    exit()

# إنشاء نسخة احتياطية
backup_file = os.path.join(BACKUP_PATH, file_name)
shutil.copy(downloaded_file, backup_file)
print(f"Backup created: {backup_file}")

# إرسال إشعار بالبريد الإلكتروني
def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = email_receiver

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# استدعاء الدالة بعد اكتمال التحميل
send_email("Notification: Download Succeeded", f"File saved in: {downloaded_file}")
