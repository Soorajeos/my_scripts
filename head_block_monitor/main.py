import requests
import datetime
from time import sleep
import smtplib
from email.message import EmailMessage

telegram_token = "1539694150:AAHqExjdXP_P9_yYMxJBlc6mG5LkyCkPnlE"
chat_id = "-1001264934506"


def send_email(subject, message):
    msg = EmailMessage()

    my_address = "sooraj@eosdublin.com" # sender's

    app_generated_password = "uovonmgkakajhaqp"  # Not password of gmail(app password)

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


url = "https://api.eosdublin.io/v1/chain/get_info"

response = requests.get(url=url)

kill_trigger = 0
while bool(response) is False:
    sleep(600)
    response = requests.get(url=url)

    if kill_trigger > 4:
        kill_message = "Unable to request, The server seems to be down \n please check " + url
        kill_subject = "The server seems to be down"

        telegram_alert(telegram_token, chat_id, kill_message)
        send_email(kill_subject, kill_message)
        exit()
    kill_trigger += 1

head_block_time = response.json()["head_block_time"]

formatted_head_block_time = " ".join(head_block_time.split("T"))
checking_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
head_time_obj = datetime.datetime.strptime(formatted_head_block_time, '%Y-%m-%d %H:%M:%S.%f')

if checking_time > head_time_obj:
    msg = "The head block time behind current time. \n The last head block time is " + str(formatted_head_block_time) + ".\n please check " + url
    subject = "The head block time issue"
    telegram_alert(telegram_token, chat_id, msg)
    send_email(subject, msg)

