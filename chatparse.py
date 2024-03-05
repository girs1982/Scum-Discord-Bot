import codecs
import datetime as dt
import os


def convert_to_date(text):
    year, month, day, hour, minute, second = [int(x) for x in text.split(".")]
    return dt.datetime(year, month, day, hour, minute, second)


def parse_chat(file_name, last_chat_dt):
    data = []
    text = codecs.open(file_name, 'r', 'utf-16-le')
    for line in text:
        if "'Global:" in line:
            event = {}
            line = line.replace(':', "'").replace("' ", "'").replace("''","'")  # replacing all extraneous delimiters to single '
            line_split = line.split("'")  # split along single '
            time_sent_date = convert_to_date(line_split[0].replace("-", "."))
            if time_sent_date > last_chat_dt:
                username = line_split[2].split("(")[0]
                channel = line_split[3]
                message = line.split("'Global'")[1]
                message = message[:len(message)-1]
                event['date'] = time_sent_date
                event['user'] = username
                event['message'] = message
                last_chat_dt = time_sent_date
                data.append(event)
    return data
