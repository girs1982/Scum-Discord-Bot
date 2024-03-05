import configparser

config = configparser.ConfigParser()
config['FTP'] = {'host': '185.70.107.19:8821',
                 'usr': 'romanc',
                 'pwd': '48h54L7q!#',
                 'path': '/185.70.107.19_7000/'}
config['DISCORD'] = {'token': 'MTE2OTc4MTk2MDY0MjY3MDU5Mg.GDQ_61.hoUnF2V5GHJIURtU7rWT2GPYfPBgfHDBLjSESU',
                     'delay': '5',
                     'kill_channel': '1213566780304527380',
                     'chat_channel': '1213566958390222868',
                     'login_channel': '1213567086224482326'}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
