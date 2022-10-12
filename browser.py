import requests
import json
from selenium import webdriver
from os import path, curdir


#Эта хуйня создана исключительно на будущее, если нужно будет автоматизировать через Долфин

dir = path.abspath(curdir)


def start_automation(profile_id=17707967):
    url = f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1"
    response = requests.request('GET', url)
    port = json.loads(response.content).get('automation').get('port')
    print('Port: ', port)
    chromedriver = f'chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.debugger_address = f'127.0.0.1:{port}'
    driver = webdriver.Chrome(chromedriver, chrome_options=options)
    driver.maximize_window()
    driver.get('https://immortal.game/play?opponent=computer')
    return driver

if __name__ == '__main__':
    driver = start_automation()
