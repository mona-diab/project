import os
import shutil
import requests
from urllib.parse import urlparse, unquote

file_url = input("Enter the file URL: ")

USER_HOME = os.path.expanduser("~")
DOWNLOAD_PATH = os.path.join(USER_HOME, "Downloads", "files")
BACKUP_PATH = os.path.join(USER_HOME, "Downloads", "backup")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
os.makedirs(BACKUP_PATH, exist_ok=True)

parsed_url = urlparse(file_url)
file_name = os.path.basename(parsed_url.path)
file_name = unquote(file_name)  
if not file_name:
    file_name = "downloaded_file"  

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

backup_file = os.path.join(BACKUP_PATH, file_name)
shutil.copy(downloaded_file, backup_file)
print(f"Backup created: {backup_file}")
