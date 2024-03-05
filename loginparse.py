import codecs
import datetime as dt


def parse_login(file_name, last_login_dt):
    text = codecs.open(file_name, 'r', 'utf-16-le')
    usernames = []
#    last_login_dt_str = last_login_dt.strftime("%Y.%m.%d.%H.%M.%S.%f")[:-3]
#    last_login_dt = dt.datetime.strptime(last_login_dt_str, "%Y.%m.%d.%H.%M.%S")
    last_login_dt = last_login_dt.replace(microsecond=0)
    for line in text:
        #print(line)
        if "logged in" in line:
            event = {}
            
            line = line.split("'")
            line[0] = line[0].split(":")[0]
            line[0] = line[0].replace("-", ".")
            year, month, day, hour, minute, second = [int(x) for x in line[0].split(".")]
            user_info = line[1].replace(" ", ",").replace(":", ",").split(",")[2]
            print(user_info)
            #date = dt.datetime(year, month, day, hour, minute, second)
            date_str = line[0].split(":")[0].replace("-", ".")
            date = dt.datetime.strptime(date_str, "%Y.%m.%d.%H.%M.%S")
            print(date)
            print(last_login_dt)
            # Добавим проверку на None для last_login_dt
            if last_login_dt is None or date > last_login_dt:
                event['user'] = user_info.split("(")[0]
                event['date'] = dt.datetime(year, month, day, hour, minute, second)
                usernames.append(event)
                print("worka")
                
                # Обновим last_login_dt только в случае успешного добавления события
                last_login_dt = date
    
    return usernames
