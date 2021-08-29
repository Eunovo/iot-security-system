import requests


class Logger:
    def __init__(self, url):
        self.url = url

    def log(self, message):
        try:
            requests.get(self.url, params={'nessage': message})
        except:
            print('Could not log message')
