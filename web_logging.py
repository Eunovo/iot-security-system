import requests


class Logger:
    def __init__(self, url):
        self.url = url

    def log(self, message):
        try:
            print(message);
            requests.get(self.url, params={'message': message})
        except:
            print('Could not log message')
