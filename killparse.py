import json
import codecs
import datetime as dt


def get_sector_letter(yCoord):
    z_top = -601147
    a_top = -295542
    b_top = 96889
    c_top = 315295

    if yCoord < z_top:
        return "Z"
    elif yCoord < a_top:
        return "A"
    elif yCoord < b_top:
        return "B"
    elif yCoord < c_top:
        return "C"
    else:
        return "D"


def get_sector_number(xCoord):
    four_right = 314922
    three_right = 9130
    two_right = -295915
    one_right = -601147

    if xCoord > four_right:
        return "4"
    elif xCoord > three_right:
        return "3"
    elif xCoord > two_right:
        return "2"
    elif xCoord > one_right:
        return "1"
    else:
        return "0"


def convert_to_date(date):
    date = date.replace("-", ".")
    year, month, day, hour, minute, second = [int(x) for x in date.split(".")]
    return dt.datetime(year, month, day, hour, minute, second)


def parse_kill(file_name, last_kill_dt):
    data = []
    text = codecs.open(file_name, 'r', 'utf-16-le')
    for line in text:
        event = {}
        if "." in line:
            date = line.split(":")[0]
            date = date.replace("-", ".")
            print(date)
            date = convert_to_date(date)
            content = line[21:]
            if content.startswith("{") and date > last_kill_dt:
                json_doc = json.loads(content)
                killer = json_doc["Killer"]
                victim = json_doc["Victim"]
                killer_name = killer["ProfileName"]
                victim_name = victim["ProfileName"]
                event['killer'] = killer_name
                event['killerLoc'] = get_sector_letter(killer["ServerLocation"]["X"]) + get_sector_number(
                    killer["ServerLocation"]["Y"])
                event['victim'] = victim_name
                event['victimLoc'] = get_sector_letter(victim["ServerLocation"]["X"]) + get_sector_number(
                    victim["ServerLocation"]["Y"])
                event['weapon'] = json_doc["Weapon"]
                last_kill_dt = date
                event['date'] = date
                data.append(event)
    return data
