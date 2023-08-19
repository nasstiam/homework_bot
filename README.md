# Telegram-bot

### Description
Telegram bot is checking homework statuses in Yandex Practicum.
Send initiall statuses of homeworks and further changes.


### Technology stack:  
Python 3.7  
python-dotenv 0.19.0  
python-telegram-bot 13.7 


### How to start a project:
Clone repository and change to it on the command line:

```
git clone git@github.com:nasstiam/homework_bot.git
cd homework_bot
```
Create virtual environment:

```
python -m venv venv
```
Activate virtual environment:
```
source venv/Scripts/activate
```
Install dependencies from requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```


Write the necessary keys to environment variables (file .env):

- PRACTICUM_TOKEN - profile token on Yandex.Practicum
- TELEGRAM_TOKEN - telegram-bot token
- TELEGRAM_CHAT_ID - сyour telegram ID

Run project:
```
python homework.py
```

