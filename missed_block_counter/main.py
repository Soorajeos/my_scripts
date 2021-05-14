import time
import subprocess
import select
import sys
import smtplib
from email.message import EmailMessage
import requests

filename = sys.argv[1]

telegram_token = "Telegram Api"
chat_id = "Telegram Chat Id"


def send_email(subject, message):
    msg = EmailMessage()

    my_address = "sooraj@eosdublin.com"  # sender's

    app_generated_password = "App password"  # Not password of gmail(app password)

    msg["Subject"] = subject

    msg["From"] = my_address

    msg["To"] = "sooraj@eosdublin.com"  # receiver's

    msg.set_content(message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(my_address, app_generated_password)

        smtp.send_message(msg)

        smtp.close()


def telegram_alert(token, chatid, message):
    telegram_url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(token, chatid, message)
    requests.post(url=telegram_url, timeout=10)


f = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

temp = 0

while True:
    if p.poll(1):
        try:
            data = str(f.stdout.readline()).split("@")[0].split("#")[1]
            my_list = []
            my_list.append(int(data))
            for i in my_list:
                if temp == 0:
                    temp = i
                elif i - temp == 1:
                    temp = i

                elif i - temp > 1:
                    msg = "The blocks has been missed between ", temp, " and ", i
                    sub = "MISSED BLOCK"
                    telegram_alert(telegram_token, chat_id, msg)
                    send_email(sub, msg)
                    temp = i
        except:
            pass
        time.sleep(1)
