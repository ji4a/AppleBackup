import os
import tarfile
import datetime
from ftplib import FTP

def count_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

// CHANGE DIRECTORY PATH
source_directory = 'ABSOLUTE_PATH_HERE'

// CHANGE FTP CREDENTIALS
ftp_host = ''
ftp_username = ''
ftp_password = ''
ftp_directory = ''

backup_folder = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

backup_filename = f'{backup_folder}.tar.gz'
backup_path = os.path.join(source_directory, backup_filename)

# Count the number of files in the source directory
total_files = count_files(source_directory)
processed_files = 0
prev_percentage = -1

# Create a tar.gz archive of the source directory
with tarfile.open(backup_path, 'w:gz') as tar:
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            processed_files += 1
            percentage = min(int((processed_files / total_files) * 100), 100)
            if percentage != prev_percentage:
                progress_bar = '[' + ('#' * (percentage // 10)).ljust(10) + ']'
                print(f'\rBackup progress: {progress_bar} {percentage}% ', end='')
                prev_percentage = percentage
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, source_directory)
            tar.add(filepath, arcname=arcname)

print('\nBackup created successfully!')

def progress_callback(block):
    global prev_percentage
    uploaded = file.tell()
    percentage = min(int((uploaded / file_size) * 100), 100)
    if percentage != prev_percentage:
        progress_bar = '[' + ('#' * (percentage // 10)).ljust(10) + ']'
        print(f'\rUpload Progress: {progress_bar} {percentage}% ', end='')
        prev_percentage = percentage

with FTP(ftp_host) as ftp:
    ftp.login(user=ftp_username, passwd=ftp_password)
    ftp.cwd(ftp_directory)
    with open(backup_path, 'rb') as file:
        file_size = os.path.getsize(backup_path)
        ftp.storbinary(f'STOR {backup_filename}', file, callback=progress_callback)

print('\nBackup uploaded successfully!')

os.remove(backup_path)
