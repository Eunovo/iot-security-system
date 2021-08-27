import requests


def log(url, message):
    try:
        requests.get(url, params={'nessage': message})
    except:
        print('Could not log message')
