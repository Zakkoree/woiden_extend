"""
    BYPASS reCaptcha By YouTube Channel: NIKO TECH
    Captcha + Others By github@Mybdye 2022.03.24
"""

import os
import sys
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import captcha
import globalVal
from commonlog import Logger

authRetry = 0
extendRetry = 0
retryNum = 3

# secret
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

# origin_host = 'hax.co.id'

origin_host = "woiden.id"
renew_path = "/vps-renew"
login_path = "/login"
info_path = "/vps-info"
google_recaptchaV3_js_path = "/dist/js/renew-vps.js"

logger = Logger(LoggerName = "HaxExtend")

def delay():
    time.sleep(random.randint(2, 10))


def barkPush(body):
    # bark push
    # barkUrl = 'https://api.day.app/' + BARKKEY
    # title = 'HaxExtend'
    # requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
    try:
        WXURL = os.environ['WXURL']
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{origin_host}:{body}"
            }
        }
        requests.post(WXURL,json=data)
    except:
        return
    
def adsClear():
#     print("[INFO] clear adsbygoogle")
    logger.info("clear adsbygoogle")
    try:
        globalVal.driver.execute_script("$('ins.adsbygoogle').css('display','none');")
    except Exception as e:
        return
    
def openUrl():
    logger.info("load " + origin_host)
#     print("[INFO] load " + origin_host)
    globalVal.driver.get('https://' + origin_host + login_path)
    delay()
    
    adsClear()
    
    # globalVal.driver.switch_to.window(globalVal.driver.window_handles[0])
#     print('[INFO] fill username')
    logger.info("fill username")
    globalVal.driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(USERNAME)
#     print('[INFO] fill password')
    logger.info("fill password")
    globalVal.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
    
def extend():
    global extendRetry
    logger.info("click Extend VPS")
#     print('[INFO] click Extend VPS')
#     Extend VPS Expiration
#     WebDriverWait(globalVal.driver, 30).until(
#         EC.visibility_of_element_located((By.LINK_TEXT, 'RENEW'))).click()
    globalVal.driver.get('https://' + origin_host + renew_path)

#     aaa = globalVal.driver.find_element(By.LINK_TEXT, 'RENEW')
#     globalVal.driver.execute_script("arguments[0].click();", aaa)
    delay()
    # 验证码V3
    captcha.recaptchaV3()
    adsClear()
    
    # input web address
    logger.info("fill web address")
#     print('[INFO] fill web address')
    globalVal.driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys(origin_host)
    delay()
    # captcha
#     print('[INFO] do CAPTCHA')
    logger.info("do CAPTCHA")
    globalVal.driver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(captcha.numCAPTCHA())
    delay()
    # agreement check
    logger.info("click agreement")
#     print('[INFO] click agreement')
    globalVal.driver.find_element(By.NAME, 'agreement').click()
    
    delay()
    
    # reCAPTCHA again
    # print('do reCAPTCHA')
    # reCAPTCHA()
    # time.sleep(10)
    # globalVal.driver.switch_to.default_content()
    # submit_button (Renew VPS)
#     print('[INFO] click Renew VPS')
    logger.info("click Renew VPS")
    globalVal.driver.find_element(By.NAME, 'submit_button').click()
    time.sleep(20)
#     print('[INFO] copy text')
    logger.info("copy text")
    body = WebDriverWait(globalVal.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
#     txt = globalVal.driver.execute_script("return $('#form-submit').html()")
#     logger.info("copy text:" + str(txt))
    # print('textBody:', body)
    delay()
    extendState = "failed" in body
    login = "log" in body
    if login:
        logger.warn("You have to log in!")
        sys.exit()
    logger.info("bark push " + str(body))
    
#     print('[INFO] bark push',body)
    
    
    
    # 重试次数和无限次二选一
    
    
    # 续订固定重试次数
    if extendState:
        extendRetry += 1
        if extendRetry >= retryNum+1:
            return False
        logger.info("try renew "+ str(extendRetry))
#         print('[INFO] try renew '+ str(extendRetry))
        delay()
        extendState = extend()
        
    else:
        return True
    
    # 无限执行续订
#     if extendState:
#         logger.error("renew fail")
#     else:
#         logger.info("renew succeed")
#     extend()
#     time.sleep(60*10)

    
def run():
    global authRetry
    openUrl()
    # reCAPTCHA
    logger.info("do reCAPTCHA")
#     print('[INFO] do reCAPTCHA')
    re = captcha.reCAPTCHA()
    
    if re == 2:
       openUrl()
       captcha.twoCaptcha()
    elif re == 3:
        if authRetry >= retryNum+1:
            logger.error("login fail!")
#             print('[ERROR] login fail!')
            return
        authRetry += 1
        logger.info("try login "+ str(authRetry))
#         print('[INFO] try login '+ str(authRetry) )
        run()
        return
    time.sleep(10)
    # login
    globalVal.driver.switch_to.default_content()
#     print('[INFO] click login')
    logger.info("click login")
    login_btn = globalVal.driver.find_element(By.NAME, 'login')
#     globalVal.driver.execute_script("arguments[0].scrollIntoView();", login_btn)
#     login_btn.click()
    globalVal.driver.execute_script("arguments[0].click();", login_btn)
    time.sleep(10)
    logger.info("skip the ads")
#     print("[INFO] skip the ads")
    globalVal.driver.get('https://' + origin_host + renew_path)
    
    delay()
    
    adsClear()
    # Extend VPS link
    extendState = extend()
    
    if extendState:
        logger.info("renew succeed")
#         print('[INFO] renew succeed')
        barkPush('[INFO] renew succeed')
    else:
        logger.error("renew fail")
#         print('[ERROR] renew fail')
        barkPush('[ERROR] renew fail')
    delay()


if __name__ == '__main__':
    try:
        # create chrome driver
        Options = webdriver.ChromeOptions()
        Options.add_argument('--headless')
        # Options.add_extension('./adguard.crx')
        Options.add_argument('--no-sandbox')
        Options.add_argument('--disable-gpu')
        Options.add_argument('--disable-dev-shm-usage')
        globalVal.driver = webdriver.Chrome(options=Options)
        delay()
        # go to website which have recaptcha protection
    except Exception as e:
#         print(e)
        logger.error(e)
        logger.error("[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")
        sys.exit()
    run()
    globalVal.driver.quit()
