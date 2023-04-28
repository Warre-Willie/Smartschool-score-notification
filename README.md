# Smartschool score notification

You will receive a notification via Telegram with you rresult for every new point within 10 minutes.  
I'm rewriting the code to make it look prettier.

## Requirements  
* **Linux server**
* Smartschool account
* Telegram account

## Installation of packages
_follow the step by step instruction for easy installation. In case of problems, create a Github issue._
### Install Google Chrome
1. Download Google chrome:
   ```sh
   wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   ```
2. Update all packages
   ```sh
   sudo apt update
   ```
3. Install Google Chorme
   ```sh
   sudo apt install -f ./google-chrome-stable_current_amd64.deb
   ```
4. Install git
   ```sh
   sudo apt install git
   ```

### Install Python Selenium webdriver
1. If you don't have Python installed yet, do this first. Otherwise, you can just move on.
2. Install Python pip
   ```sh
   sudo apt install python3-pip
   ```
3. Install Selenium webdriver
   ```sh
   pip install selenium webdriver-manager
   ```
## Telegram bot  
### Get BOT_TOKEN ([Telegram doc](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))
1. Start a chat with **@BotFather**
2. Send `/start` and follow the instructions to create a bot
3. Copy the bot token to use later
4.  Search your bots username in Telegram to start a chat. And send `/start`
### Get CHAT_ID  
1. Start a chat with **@TelegramBotRaw**
2. Send `/start`
3. Look for `chat_id = xxxxxxxxxx` and copyt this to use later

## Install the program
1. Donwload all the files from Github
   ```sh
   git clone https://github.com/Warre-Willie/Smartschool-score-notification.git
   ```
3. Go inside the folder with all the files
   ```sh
   cd Smartschool-score-notification/
   ```
### Configuration
1. Open the config file
   ```sh
   sudo nano config.ini
   ```
2. Replace tha data with your personal info  
   **Don't type "" for your data and dant leave any spaces behind the data**  
   * BOT_TOKEN = your Telegram bot token
   * CHAT_ID = your Telegram chat id
   * Smartschool_URL = the name of your school in front of `.smartschool.be´ in the URL when you login
   * USERNAME = Smartschool username
   * PASSWORD = Smartschool password
   * TIME_INTERVAL = in minutes, the time to wait before checing for new points
   
3. Save the script by pressing `Ctrl + O` and hit `Enter`
4. Close the script by pressing `Ctrl + X` 

## Test program
```sh
python3 smartschool-score-notification.py
```
Press `Ctrl + C` to end the test.
If should recieve a message from your bot. If you get a ERROR in the terminal please create a Github issue.  

## Run in background
To run the program in the background so you can close the terminal please follow following instuctions.

### Start process
Make sure you are in the same folder where all the files are.
```sh
nohup python3 smartschool-score-notification.py > smartschool.out&
```
You should get a Telegram message again.

### Stop process
Get the process_id of the background process
```sh
ps -ef | grep smartschool-score-notification.py
```
Output should look something like this
```sh
python-+    xxxx    4797  0 19:21 pts/4    00:00:00 python3 smartschool-score-notification.py`
```
The xxxx is the process_id of your script.  

Replace xxxx with you process_id to end the script
```sh
kill xxxx
```
