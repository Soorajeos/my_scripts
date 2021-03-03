import requests
import datetime
from time import sleep
import smtplib
from email.message import EmailMessage


def send_email(subject, message):
    msg = EmailMessage()

    my_address = "sooraj@eosdublin.com"  # sender's

    app_generated_password = "uovonmgkakajhaqp"  # Not password of gmail(app password)

    msg["Subject"] = subject

    msg["From"] = my_address

    msg["To"] = "sooraj@eosdublin.com"  # receiver's

    msg.set_content(message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(my_address, app_generated_password)

        smtp.send_message(msg)

        smtp.close()


url = "http://snapshots.eosdublin.io/wax/"

response = requests.get(url=url)
text_data = response.text
kill_trigger = 0
while bool(response) is not True:
    sleep(5)
    # print("request error ")
    response = requests.get(url=url)
    text_data = response.text
    if kill_trigger >= 5:
        kill_subject = "REQUEST ERROR"
        kill_message = "The snapshot server seems to be down. Please check the server"
        # send email
        send_email(kill_subject, kill_message)
        exit()
    kill_trigger += 1
data = text_data.splitlines()

date_list = []

for i in data:
    try:
        date_list.append(i.split("</a>")[1])
    except:
        pass

latest_date = date_list[-1].split(" ")[1]
checking_date = (datetime.datetime.now().date() - datetime.timedelta(days=2)).strftime("%d-%m-%Y")

if latest_date < checking_date:
    subject = "Snapshot error "
    message = "seems like the latest snapshot is not created. The last snapshot was created on : " + latest_date
    send_email(subject, message)
