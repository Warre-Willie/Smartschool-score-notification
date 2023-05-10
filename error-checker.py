# __      __                                __      __.__.__  .__                         
#/  \    /  \_____ ______________   ____   /  \    /  \__|  | |  |   ____   _____   ____  
#\   \/\/   /\__  \\_  __ \_  __ \_/ __ \  \   \/\/   /  |  | |  | _/ __ \ /     \_/ __ \ 
# \        /  / __ \|  | \/|  | \/\  ___/   \        /|  |  |_|  |_\  ___/|  Y Y  \  ___/ 
#  \__/\__/  (______/__|   |__|    \_____>   \__/\__/ |__|____/____/\_____>__|_|__/\_____> 

import configparser
import requests
import time

from datetime import datetime
from datetime import timedelta

config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

TELEGRAM = config['TELEGRAM']
BOT_TOKEN = TELEGRAM['BOT_TOKEN']
CHAT_ID = TELEGRAM['CHAT_ID']

SETTINGS = config['SETTINGS']
TIME_INTERVAL = SETTINGS['TIME_INTERVAL']
time_interval = datetime.strptime(TIME_INTERVAL, "%H:%M:%S")
time_interval = timedelta(
  days=0,
  hours=time_interval.hour,
  minutes=time_interval.minute,
  seconds=time_interval.second,
)

SLEEP_ENABLED = SETTINGS['SLEEP_ENABLED']
START_SLEEP = SETTINGS['START_SLEEP']
STOP_SLEEP = SETTINGS['STOP_SLEEP']
start_sleep = datetime.strptime(START_SLEEP, "%H:%M")
stop_sleep = datetime.strptime(STOP_SLEEP, "%H:%M")
sleep_time = stop_sleep - start_sleep

if sleep_time.days < 0:
    sleep_time = timedelta(
        days=0,
        seconds=sleep_time.seconds,
    )
error_state = False
while error_state == False:
    out_file = open("smartschool.out", "r")
    data = out_file.read()
    if data.find("Traceback (most recent call last):") != -1:
        error_state = True
        while True:
            response = requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Program stopped check smartschool.out file for more information'.format(BOT_TOKEN, CHAT_ID))
            if response.status_code == 200:
                exit()
    if data.find("[WDM] - Downloading:") != -1:
        out_file.close()
        out_file = open("smartschool.out", "a")
        out_file.truncate(0)
    out_file.close()
    currentDateAndTime = datetime.now()
    if(int(currentDateAndTime.hour) == start_sleep.hour and SLEEP_ENABLED):
        time.sleep(sleep_time.total_seconds())
    time.sleep(time_interval.total_seconds())
