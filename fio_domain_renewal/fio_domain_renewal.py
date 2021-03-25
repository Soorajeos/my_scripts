import requests


telegram_token = "Telegram api key "
chat_id = "Telegram chat id"


# sends telegram alert
def telegram_alert(token, chatid, message):
    telegram_url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(token, chatid, message)
    requests.post(url=telegram_url, timeout=10)


try:
    # The url of api server comes here
    url = "https://testnet.fioprotocol.io/v1/chain"

    # url of api server (endpoint : get_fee)
    fee_url = url + '/v1/chain/get_fee'
    fee_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    # the address has to be changed.
    fee_data = '{"end_point":"renew_fio_domain","fio_address":"alice@purse"}'

    fee_response = requests.post(url=fee_url, headers=fee_headers, data=fee_data)
    max_fee = fee_response.json()["fee"]

    renewal_url = url + '/v1/chain/renew_fio_domain'

    renewal_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    # using the max_fee obtained from the above response. The doman , tpid and actor has to be edited.
    renewal_data = '{"fio_domain": "string", "max_fee":' + str(max_fee) + ', "tpid": "string", "actor": "string"}'

    response = requests.post(url=renewal_url, headers=renewal_headers, data=renewal_data)
    expiration_data = response.json()["expiration"]
    renewal_status = response.json()["status"]

    if renewal_status == "OK":
        message = "The domain is renewed till " + expiration_data
        telegram_alert(telegram_token, chat_id, message=message)
    else:
        msg = "something went wrong. Status : " + renewal_status
        telegram_alert(telegram_token, chat_id, message=msg)
except :
    kill_msg = "The domain is not registered. Please check."
    telegram_alert(telegram_token, chat_id, message=kill_msg)
    
