# __      __                                __      __.__.__  .__                         
#/  \    /  \_____ ______________   ____   /  \    /  \__|  | |  |   ____   _____   ____  
#\   \/\/   /\__  \\_  __ \_  __ \_/ __ \  \   \/\/   /  |  | |  | _/ __ \ /     \_/ __ \ 
# \        /  / __ \|  | \/|  | \/\  ___/   \        /|  |  |_|  |_\  ___/|  Y Y  \  ___/ 
#  \__/\__/  (______/__|   |__|    \_____>   \__/\__/ |__|____/____/\_____>__|_|__/\_____> 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from datetime import datetime
from datetime import timedelta

import requests
import time
import os
os.system('nohup python3 nscript-error-checker.py > error.out&')
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
TELEGRAM = config['TELEGRAM']
BOT_TOKEN = TELEGRAM['BOT_TOKEN']
CHAT_ID = TELEGRAM['CHAT_ID']

SMARTSCHOOL = config['SMARTSCHOOL']
SCHOOL_NAME = SMARTSCHOOL['SCHOOL_NAME']
USERNAME = SMARTSCHOOL['USERNAME']
PASSWORD = SMARTSCHOOL['PASSWORD']

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
try:
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

  driver.get('https://{}.smartschool.be'.format(SCHOOL_NAME))
  username_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "login_form__username")))
  username_field = driver.find_element(By.ID, "login_form__username")
  password_field = driver.find_element(By.ID, "login_form__password")

  username_field.send_keys(USERNAME)
  password_field.send_keys(PASSWORD)

  password_field.submit()
  username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "smscMain")))
except:
  requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Login failed: username, password or school name is not correct'.format(BOT_TOKEN, CHAT_ID))
  print("login fail")
  exit()

requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Program started. Settings: school: {}, username: {}, pause: {}, sleep time: {}'.format(BOT_TOKEN, CHAT_ID, SCHOOL_NAME, USERNAME, TIME_INTERVAL, sleep_time))

old_html = "EMPTY"
old_points_list = ["EMPTY"]

def get_html():
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

  driver.get('https://{}.smartschool.be/results/main/table/'.format(SCHOOL_NAME))
  username_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "login_form__username")))
  username_field = driver.find_element(By.ID, "login_form__username")
  password_field = driver.find_element(By.ID, "login_form__password")

  username_field.send_keys(USERNAME)
  password_field.send_keys(PASSWORD)

  password_field.submit()

  time.sleep(5)
  filter_del_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@class="reset-filters-btn"]')))
  time.sleep(5)
  filter_del_button.click()
  html = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "td")))  
  html = driver.page_source
  driver.close()

  html = html.split('<table class="table-page__container__wrapper__table js-results-table">', 2)
  html = html[1].split('</table></div></div></div>', 2)
  html = html[0]
  return(html)

def split_points(new_html):
  points_list = []
  points_row = new_html.split('<tr class="row row--course js-row-course">')
  if(points_row[0] == ''):
    del points_row[0]

  for elem in points_row: 
    elem_split = elem.split("</tr>")
    points_row[points_row.index(elem)] = elem_split[0]

  for row in points_row:
    row_points = row.split('</span></div></td>', 2)
    del row_points[0]
    row_points = row_points[0].split('</td>')
    del row_points[len(row_points) - 1]
    for point in row_points:
          if(point == '<td class="cell cell--spacer">&nbsp;'):
              del row_points[row_points.index(point)]
          else:
              points_list.append(point)
  return(points_list)

def comp_points(points_list, old_points_list):
  result = []
  for elem in points_list:
    if elem not in old_points_list:
      result.append(elem)
  old_points_list = points_list
  return(result)

def get_result(result):
  identifiers = []
  for elem in result:
    elem = elem.split('<button evaluation-identifier="')
    elem = elem[1].split('" class="evaluation__content')
    identifiers.append(elem[0])
  for elem in identifiers:
    identifiers[identifiers.index(elem)] = "https://{}.smartschool.be/results/main/results/details/".format(SCHOOL_NAME) + elem

  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

  subjects = []
  for elem in identifiers:
    driver.get(elem)
    if(identifiers.index(elem) == 0):
      username_field = driver.find_element(By.ID, "login_form__username")
      password_field = driver.find_element(By.ID, "login_form__password")
      username_field.send_keys(USERNAME)
      password_field.send_keys(PASSWORD)
      password_field.submit()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='side-panel__content__score side-panel__content__score--percentage']"))) # Wait for the result to load
    img_container = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='side-panel__panel']")))
    time.sleep(3) #Time to let the animation load for the screenshot
    
    img_container.screenshot("result_{}.png".format(identifiers.index(elem)))
    img = Image.open("result_{}.png".format(identifiers.index(elem)))

    img_crop = img.crop((0, 0, (img.width - 100), 274))
    img_crop = img_crop.save("result_{}.png".format(identifiers.index(elem)))

    subject = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='blob-group']/div[2]/div[2]/span")))
    if(subject.text not in subjects):
      subjects.append(subject.text)
  driver.close()  
  send_results(identifiers, subjects)

def send_results(identifiers, subjects):
  subject_string = "Nieuwe punten van "
  for elem in identifiers:
    if(len(subjects) == 1):
      subject_string = "Nieuw punt van " + subjects[0]
    elif(len(subjects) == 2):
      subject_string += subjects[0] + " en " + subjects[1]
    else:
      for subject in subjects:
        if(subjects.index(subject) != (len(subjects) - 1 )):
          if(subjects.index(subject) != 0):
            subject_string += ", " + subject
          else:
            subject_string += subject
        else:
            subject_string += " en " + subject
    del subjects

  for elem in identifiers:
    files = {'photo':open("result_{}.png".format(identifiers.index(elem)), 'rb')}
    if(identifiers.index(elem) == (len(identifiers) - 1)):
      requests.post('https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption={}'.format(BOT_TOKEN, CHAT_ID, subject_string), files=files)
    else:
      time.sleep(2)
      requests.post('https://api.telegram.org/bot{}/sendPhoto?chat_id={}&disable_notification=true'.format(BOT_TOKEN, CHAT_ID), files=files)
    os.remove("result_{}.png".format(identifiers.index(elem)))
  del identifiers

while True:
  new_html = get_html()
  if(old_html == "EMPTY"):
    old_html = new_html
    old_points_list = split_points(old_html)
  if(new_html != old_html):
    points_list = split_points(new_html)
    result = comp_points(points_list, old_points_list)
    result = get_result(result)
  old_html = new_html
  currentDateAndTime = datetime.now()
  if(int(currentDateAndTime.hour) == start_sleep.hour and SLEEP_ENABLED):
    time.sleep(sleep_time.total_seconds())
  time.sleep(time_interval.total_seconds())