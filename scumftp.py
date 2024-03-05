import ftplib
import configparser
import datetime as dt
import os
from datetime import datetime
def convert_to_datetime(date_str, time_str):
    # Парсим дату
    date_parts = date_str.split('-')
    month = int(date_parts[0])
    day = int(date_parts[1])
    year = 2000 + int(date_parts[2])  # Предполагаем, что год в диапазоне 2000-2099

    # Парсим время
    time_parts = time_str[:-2].split(':')  # Исключаем последние два символа (AM/PM)
    hour = int(time_parts[0])
    minute = int(time_parts[1])

    # Учитываем AM/PM
    if time_str.endswith('PM') and hour != 12:
        hour += 12

    return datetime(year, month, day, hour, minute)



def check_files(ftp_info, last_chat_dt, last_kill_dt, last_login_dt):
    new_files = []
    ftps = ftplib.FTP()
    ftps.connect(ftp_info['host'], int(ftp_info['port']))
    ftps.login(ftp_info['usr'], ftp_info['pwd'])
    ftps.cwd(ftp_info['path'])

    data = []
    ftps.retrlines("LIST", data.append)  # Получаем строки содержимого каталога

    for line in data:
        file_info = line.split(None, 8)
        #print(file_info[-1])
        if len(file_info) < 4:
            continue
        file_name = file_info[-1]
        date_str = file_info[0]
        time_str = file_info[1]
#        print(date_str)
#        print(time_str)
        modified_date = convert_to_datetime(date_str, time_str)
        

        #modified_date_str = f"{file_info[0]} {file_info[1]} {file_info[2]}"
#        modified_date = convert_to_datetime(modified_date_str)
#        print(f"File: {file_name}, Modified Date: {modified_date}")

        # Остальная логика обработки файлов
        if file_name.startswith("chat_"):
            if modified_date > last_chat_dt:
                new_files.append(file_name)
        elif file_name.startswith("kill_"):
            if modified_date > last_kill_dt:
                new_files.append(file_name)
        elif file_name.startswith("login_"):
            if modified_date > last_login_dt:
                new_files.append(file_name)

    for file in new_files:
#         downloaded_files = []
         with open(file, "wb") as wfile:
            try:
                ftps.retrbinary('RETR %s' % file, wfile.write)
#               downloaded_files.append(file)
                print(f"File {file} downloaded successfully.")
            except Exception as e:
                print(f"Error downloading file {file}: {e}")
#         with open(file, "r") as rfile:
#             content = rfile.read()
#             print(f"Content of {file}:\n{content}")
    return new_files

def delete_files(files):
    for i in range(len(files)):
        print("deleting ", files[i])
#        try:
#            print("deleting ", file)
            #ftp.delete(files[i])
#        except Exception as e:
#            print(f"Error deleting file {file} from FTP: {e}")
        os.remove(files[i])

