import requests
import dateparser
import smtplib
import datetime
from time import sleep
from email.message import EmailMessage


def send_email(subject, message):
    msg = EmailMessage()

    my_address = "EMAIL"  #sender's

    app_generated_password = "APP_PASSWORD"  # Not password of gmail(app password)

    msg["Subject"] = subject

    msg["From"] = my_address

    msg["To"] = "EMAIL_ID"   # receiver's

    msg.set_content(message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(my_address, app_generated_password)

        print("sending mail alert")
        smtp.send_message(msg)
        print("mail has sent")
        smtp.close()


# Headers comes here
headers = {
    'Content-Type': 'application/json',
}

data = '{"limit" : "100", "json" : true}'
url = 'https://api.eosdublin.io/v1/chain/get_producers'     # url comes here

response = requests.post(url=url, headers=headers, data=data)

kill_trigger = 0
while bool(response) is not True:
    print("ERROR OCCURED.....")
    if kill_trigger == 6:
        kill_subject = "Api seems to be down"
        kill_message = "The program has been aborted. Api Node seems to be down  "
        send_email(kill_subject, kill_message)
        exit()

    response = requests.post(url=url, headers=headers, data=data)
    sleep(1800)
    kill_trigger += 1

json_data = response.json()['rows']


# print("printing the details")


def check_status():
    for item in json_data:
        if item["owner"] == "eosdublinwow":
            print("already in the list")

            if dateparser.parse(item["last_claim_time"]).date() < (
                    datetime.datetime.now().date() - datetime.timedelta(days=1)):
                subject_new = "The last claim time "
                message_new = "The last claim of " + str(item["owner"]) + " is " + str(
                    dateparser.parse(item["last_claim_time"]))

                send_email(subject_new, message_new)
            # print("assuming claimed ")
            return True
        else:
            continue
    return False


if not bool(check_status()):
    subject = "Not in the list"
    message = "We are not listed yet "
    send_email(subject, message)
