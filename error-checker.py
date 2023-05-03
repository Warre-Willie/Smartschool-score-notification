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
    out_file = open("smartschool.out", "r").read()
    if out_file.find("error") != -1:
        error_state = True
        while True:
            response = requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Program stopped check smartschool.out file for more information'.format(BOT_TOKEN, CHAT_ID))
            if response.status_code == 200:
                break
    currentDateAndTime = datetime.now()
    if(int(currentDateAndTime.hour) == 22):
        time.sleep(sleep_time.total_seconds())
    time.sleep(time_interval.total_seconds())
