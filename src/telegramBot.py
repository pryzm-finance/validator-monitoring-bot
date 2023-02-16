from urllib.parse import quote
import requests
from datetime import datetime
#bot token should be inserted here
token="To Be Added"

#your channel id for validator monitror
channel_id="To Be Added"

#your chat id for verbose messages.
verbose_chat_id="To Be Added"
link="https://api.telegram.org/bot"+token

def sendmessage(msg):
    try:
        sendlink = "{}/sendMessage?chat_id={}&text={}".format(link,channel_id,msg)
        # print(sendlink+msg)
        requests.get(sendlink)
    except Exception as e:
        print("Error Sending telegram message")
        
def sendmessage_moein(msg):
    try:
        sendlink = "{}/sendMessage?chat_id={}&text={}".format(link,verbose_chat_id,msg)
        # print(sendlink+msg)
        requests.get(sendlink)
    except Exception as e:
        print("Error Sending telegram message")

def get_updates():
    link="https://api.telegram.org/bot{}/getUpdates".format(token)
    return requests.get(link).json()


def botMsg(msg):
    if (len(msg) > 0):
        sendmessage(prepare_msg(msg))
        verboseMsg(msg)

def verboseMsg(msg):
    if (len(msg) > 0):
        sendmessage_moein(prepare_msg(str(msg)))

def getNow():
    return int(datetime.now().timestamp())

def prepare_msg(msg):
    return '{}\nUTC: {}'.format(quote(msg),getUTCTime())

def getUTCTime():
    return str(datetime.utcnow().strftime('%a, %d %b %Y, %H:%M:%S'))
