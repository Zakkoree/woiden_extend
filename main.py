"""
author: Zakkoree
"""
# python -m playwright codegen --target python -o 'my.py' -b chromium https://woiden.id/login
# 安装playwright库
# pip install playwright

# 安装浏览器驱动文件（安装过程稍微有点慢）
# playwright install-deps --with-deps
# playwright install --with-deps

import re
import os
import sys
import time
import random
import requests
import ffmpy3
import urllib
import telepot
import ibmAPI
#import xfyunAPI
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from aip import AipSpeech
from commonlog import Logger
from playwright.sync_api import Playwright, sync_playwright, expect
from twocaptcha import TwoCaptcha

GITHUB = False

# 用户信息
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

origin_host = "woiden.id"
renew_path = "/vps-renew"
login_path = "/login"
info_path = "/vps-info"
google_recaptchaV3_js_path = "/dist/js/renew-vps.js"

# 网络连接超时时间（1000ms=1s）
timeout = 1000 * 60 * 2
# 登陆重试次数
loginRetryNum = 3
# 续订重试次数  0=直到续订成功(虽然不用重新登陆验证,但不建议使用0,不可控,正常的5次以内可以成功)  
extendRetryNum = 10
# 续订重试间隔时间（秒）
intervalTime = 10

logger = Logger(LoggerName="HaxExtend")

message = None
def delay():
    time.sleep(random.randint(2, 5))

    
def send(message):
    try:
        bot = telepot.Bot(os.environ['TELE_TOKEN'])
        bot.sendMessage(os.environ['TELE_ID'], message, parse_mode=None, disable_web_page_preview=None, disable_notification=None,
                    reply_to_message_id=None, reply_markup=None)
        logger.info("Telebot push")
    except Exception as e:
        logger.error(e)

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
        requests.post(WXURL, json=data)
    except:
        return

    

def main(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(channel="chrome", headless=False)
    # browser = playwright.firefox.launch(headless=True)
    browser = playwright.webkit.launch(headless=True)
    context = browser.new_context()
    context.set_default_timeout(timeout)
    # Open new page
    page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        window.navigator.chrome = {
            runtime: {},
            // etc.
        };
        """
    page.add_init_script(js)
    
    run(page)
    context.close()
    browser.close()


def run(page):
    if reCAPTCHA(page) == False:
        loginRetry(page)
        sys.exit()

    # login
    try:
        logger.info("click login")
        with page.expect_response(re.compile(r"(/#)|(" + info_path + ")"), timeout=timeout*2) as result:
            page.get_by_role("button", name="Submit").click()
    except Exception as e:
        logger.error(e)
        loginRetry(page)
        sys.exit()
    delay()
    # 验证码V3
    tokenCode = recaptchaV3(page)
    # Extend VPS link
    extendState = extend(page, tokenCode)
    
    if extendState:
        if GITHUB:
            try:
                now = int(time.time())
                # 转换为其他日期格式，如："%Y-%m-%d %H:%M:%S"
                timeArr = time.localtime(now)
                other_StyleTime = time.strftime("%Y-%m-%d", timeArr)
                update=open('renewTime', 'w')
                update.write(other_StyleTime)
                update.close()
            except Exception as e:
                logger.error(e)
        logger.info("renew succeed")
        # barkPush('[INFO] renew succeed')
        teleinfomsg = '''
        Woiden自动续订脚本
        Woiden Renew Succeed
        {0}
        https://github.com/Zakkoree/woiden_extend
        '''.format(message)
        send(teleinfomsg)
    else:
        if GITHUB:
            try:
                update=open('renewTime', 'w')
                lastTime = file.read()
                update.close()
            except Exception as e:
                logger.error(e)
            logger.error("renew fail")
            # barkPush('[ERROR] renew fail')
            file.read()
            teleinfomsg = '''
            Woiden自动续订脚本
            Woiden renew fail
            Last Renew Time {0}
            有问题附上报错信息到 https://github.com/Zakkoree/woiden_extend/issues 发起issue
            '''.format(lastTime)
            send(teleinfomsg)
        else:
            teleinfomsg = '''
            Woiden自动续订脚本
            Woiden renew fail
            有问题附上报错信息到 https://github.com/Zakkoree/woiden_extend/issues 发起issue
            '''.format(lastTime)
            send(teleinfomsg)
            


def adsClear(page):
    logger.info("clear adsbygoogle")
    try:
        page.evaluate("$('ins.adsbygoogle').css('display','none');")
    except Exception as e:
        return

openLoginNum = 0
def openLoginUrl(page):
    global openLoginNum
    try:
        logger.info("load " + origin_host)
        page.goto('https://' + origin_host + login_path)
        adsClear(page)
        logger.info("fill username")
        page.locator("input[id=\"text\"]").fill(USERNAME)
        logger.info("fill password")
        page.locator("input[id=\"password\"]").fill(PASSWORD)
        page.click('iframe[title="reCAPTCHA"]')
        page.click('iframe[title="reCAPTCHA"]')
    except Exception as e:
        logger.error(e)
        openLoginNum += 1
        if openLoginNum <= loginRetryNum:
            logger.error(e)
            openLoginUrl(page)
        else:
            logger.error("open login url fail")
    else:
        openLoginNum = 0

authRetry = 0
def loginRetry(page):
    global authRetry
    if authRetry >= loginRetryNum + 1:
        logger.error("login fail!")
    else:
        authRetry += 1
        logger.warn("You have to log in!")
        logger.info("try login " + str(authRetry))
        run(page)

# 目前没找到recaptchaV3入口  懂得可以试试  
def recaptchaV3(page):
    return None
    logger.info("verify recaptcha v3")
    # https://woiden.id/dist/js/renew-vps.js
    chaper_url = 'https://' + origin_host + google_recaptchaV3_js_path
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
    req = Request(url=chaper_url, headers=headers) 
    html = urlopen(req)
    bs = str(BeautifulSoup(html, 'html.parser'))

    actionIndex = bs.find("action:")
    sitekeyStart = bs.find("execute(") + 9
    sitekeyEnd = actionIndex - 3
    sitekey = bs[sitekeyStart : sitekeyEnd]
    logger.info("sitekey:" + sitekey)
    actionStart = actionIndex + 8
    actionEnd = bs.find("}).then(") -1
    action = bs[actionStart : actionEnd]
    logger.info("action:" + action)

    try:
        solver = TwoCaptcha(os.environ['TWOCAPTCHA_TOKEN'])
        result = solver.recaptcha(
            sitekey=sitekey,
            url='https://' + origin_host + renew_path,
            version='v3',
            action=action,
            score=0.9
        )

    except Exception as e:
        logger.error("recaptchaV3 Service Exception")
        logger.error(e)
        return None

    else:
        logger.info("solved:" + str(result))
        
        # 一旦我们有了令牌，我们就可以执行在方法调用中引用的相同代码， .then() 并将我们的令牌作为函数调用参数传递。在2recaptcha的演示案例中，可以在javascript控制台中打开javacsript执行以下代码：
        # window.verifyRecaptcha('03AGdBq27lvCYmKkaqDdxWLfMe3****')
        
        # 下面有几个试过的方法
#         javacsript = """$("button[name='submit_button']").unbind('click').click(function(){$('#form-submit').prepend('<input type="hidden" name="token" value="{token}">');$('#form-submit').prepend('<input type="hidden" name="action" value="renew_vps">');$("html, body").animate({scrollTop:300},"slow");$("#response").html('<div class="progress" id="progress"><div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 10%"><span class="sr-only">Loading.....</span></div></div>'),$(".progress-bar").animate({ width:"25%"}),$(".progress-bar").animate({width:"55%"}),$.ajax({ type:"POST",url:"/renew-vps-process/",data: $("form.submit").serialize(),success:function (a) {$(".progress-bar").animate({ width:"70%"}),$(".progress-bar").animate({width:"100%"}),$("#response").html(a),$("#form-submit").hide(1000)},error:function(){alert("Something wrong !")}})})""".replace("{token}",  result['code'])
#         javacsript = """document.getElementById('recaptcha-token').value='{token}'""".replace("{token}",  result['code'])
#         javacsript = """document.querySelector('[name="g-recaptcha-response-100000"]').innerText='{}'""".format(result['code'])
#         page.evaluate(javacsript)
        
        return result['code']

extendRetry = 0
def extend(page, tokenCode):
    global extendRetry
    global message
    logger.info("click Extend VPS")
    page.goto('https://' + origin_host + renew_path)
    adsClear(page)
    

    if tokenCode != None:
        javacsript = """$("button[name='submit_button']").unbind('click').click(function(){$('#form-submit').prepend('<input type="hidden" name="token" value="{token}">');$('#form-submit').prepend('<input type="hidden" name="action" value="renew_vps">');$("html, body").animate({scrollTop:300},"slow");$("#response").html('<div class="progress" id="progress"><div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 10%"><span class="sr-only">Loading.....</span></div></div>'),$(".progress-bar").animate({ width:"25%"}),$(".progress-bar").animate({width:"55%"}),$.ajax({ type:"POST",url:"/renew-vps-process/",data: $("form.submit").serialize(),success:function (a) {$(".progress-bar").animate({ width:"70%"}),$(".progress-bar").animate({width:"100%"}),$("#response").html(a),$("#form-submit").hide(1000)},error:function(){alert("Something wrong !")}})})""".replace("{token}",  tokenCode)
        page.evaluate(javacsript)
    else:
        logger.info("recaptchaV3 token is none")

    # input web address
    logger.info("fill web address")
    page.locator("input[id=\"web_address\"]").fill(origin_host)
    # captcha
    logger.info("do CAPTCHA")
    page.fill("#captcha", str(numCAPTCHA(page)))
    # page.locator("input[id=\"captcha\"]").fill(captcha.numCAPTCHA(page))
    delay()
    # agreement check
    logger.info("click agreement")
    page.click(".form-check-input")

    delay()
    logger.info("click Renew VPS")

    with page.expect_response(re.compile(r"renew-vps-process"), timeout=timeout) as result:
        page.query_selector("button[name=submit_button]").click()
    logger.info("copy text")
    # body = page.waitForSelector("#response/div").text()
    loadingIndex = 0
    body = ""

    while True:
        body = page.evaluate('''()=>{return $('#response').text()}''')
        loading = "Loading" in body
        if loading:
            if loadingIndex <= 5:
                loadingIndex += 1
                time.sleep(5)
            else:
                logger.warn("bark push body Load timeout")
                return False
        else:
            break
    logger.info("bark push " + str(body))
    login = "log" in body
    
    if login:
        loginRetry(page)
        sys.exit()
    

    extendState = "failed" in body

    # 续订固定重试次数
    if extendState or loadingIndex>5:
        if extendRetryNum == 0:
            logger.info("After " + str(intervalTime) + " seconds try renew " + str(extendRetry))
            time.sleep(intervalTime)
            extend(page, tokenCode)
        else:
            extendRetry += 1
            if extendRetry >= extendRetryNum + 1:
                return False
            logger.info("After " + str(intervalTime) + " seconds try renew " + str(extendRetry))
            time.sleep(intervalTime)
            if extend(page, tokenCode):
                return True
    else:
        message = body
        return True

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def mp3_change_pcm(audioFile):
    logger.info("Audio frequency transcoding")
    outpath = os.getcwd() + "audio.pcm"
    ff = ffmpy3.FFmpeg(
        inputs={audioFile: '-y'},
        outputs={
            outpath.format(audioFile): '-acodec pcm_s16le -f s16le -ac 1 -ar 16000'}
    )
    ff.run()
    return outpath


def audioToText(audioFile):
    ASR_CHOICE = None
    try:
        ASR_CHOICE = os.environ['ASR_CHOICE']
    except:
        logger.error("ASR_CHOICE is not set, skip ASR")
            
    try:
        if ASR_CHOICE == 'BAIDU':
            APP_ID = os.environ['APP_ID']
            API_KEY = os.environ['API_KEY']
            SECRET_KEY = os.environ['SECRET_KEY']
            return baiduAPI(APP_ID, API_KEY, SECRET_KEY, mp3_change_pcm(audioFile))

        elif ASR_CHOICE == 'IBM':
            IBM_URL = os.environ['IBM_URL']
            IBM_KEY = os.environ['API_KEY']
            return ibmAPI.asr(IBM_KEY, IBM_URL, audioFile)

#        elif ASR_CHOICE == 'XFYUN':
#            XFYUN_APP_ID = os.environ['APP_ID']
#            XFYUN_API_KEY = os.environ['API_KEY']
#            XFYUN_SECRET_KEY = os.environ['SECRET_KEY']
#            return xfyunAPI.asr(APPID=XFYUN_APP_ID, APISecret=XFYUN_SECRET_KEY, APIKey=XFYUN_API_KEY, AudioFile=mp3_change_pcm(audioFile))
        else :
            logger.warn("ASR_CHOICE setup error, skip ASR")
            return None
    except Exception as e:
        logger.error(e)
        return None
            

def baiduAPI(APP_ID, API_KEY, SECRET_KEY, audioFile):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    jsonResult = client.asr(get_file_content(audioFile), 'pcm', 16000, {'dev_pid': 1737,})
    result = jsonResult['result'][0]
    logger.info("udio verify code:" + str(jsonResult))
    return result

def twoCaptcha(page):
    openLoginUrl(page)
    try:
        solver = TwoCaptcha(os.environ['TWOCAPTCHA_TOKEN'])
        g_recaptcha = page.locator(".g-recaptcha")
        sitekey = g_recaptcha.get_attribute("data-sitekey")
        result = solver.recaptcha(
            sitekey=sitekey, url='https://' + origin_host + login_path)
        logger.info("recaptcha_res" + str(result))
        page.evaluate(
            """document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(result['code']))
        logger.info("reCAPTCHA picture done")

        page.evaluate(
            """$.each($('body>div'),function(index,e){a=$('body>div').eq(index);if(a.css('z-index')=='2000000000'){a.children('div').eq(0).click()}})""")

        return True
    except Exception as e:
        logger.error(e)
        return False

def reCAPTCHA(page):
    openLoginUrl(page)
    try:
        iframe = page.frame_locator("xpath=//iframe[starts-with(@src,'https://www.recaptcha.net/recaptcha/api2/bframe')]")
        iframe.locator("#recaptcha-audio-button").click(timeout=10000)
        # get the mp3 audio file
        src = iframe.locator("#audio-source").get_attribute("src", timeout = 10000)
        logger.info("Audio src:" + str(src))
        outPath = os.getcwd() + "audio.mp3"
        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, outPath)

        # Speech To Text Conversion
        key = audioToText(outPath)
        logger.info("Recaptcha Key:" + str(key))

        # key in results and submit
        audio_response = iframe.locator("#audio-response")
        audio_response.fill(key)
        audio_response.press('Enter')

        err = iframe.locator(".rc-audiochallenge-error-message")
        if err.get_attribute("text") == "" or err.is_visible() == False:
            logger.info("reCAPTCHA audio done")
            return True

    except Exception as e:
        logger.error(e)
        logger.warn(
            "Possibly blocked by google. Change IP,Use Proxy method for requests")
        logger.info("Audio verify fail,try picture fuck reCAPTCHA")
        return twoCaptcha(page)


def numCAPTCHA(page):
    # 获取 captcha 图片链接
    number1 = int(page.query_selector(
        'xpath=//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][0])
    caculateMethod = re.sub(r"(\n)|(\t)", "", page.evaluate(
        '''() => {return $(".col-sm-3").text()}'''))[0:1]
    number2 = int(page.query_selector(
        'xpath=//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][0])

    if caculateMethod == '+':
        captcha_result = number1 + number2
    elif caculateMethod == '-':
        captcha_result = number1 - number2
    elif caculateMethod == 'X':
        captcha_result = number1 * number2
    elif caculateMethod == '/':
        captcha_result = number1 / number2

    logger.info("renewal verify code:" + str(number1) +
                str(caculateMethod) + str(number2) + '=' + str(captcha_result))
    return captcha_result


if __name__ == '__main__':
    try:
        origin_host = os.environ['HOST']
    except:
        pass
    with sync_playwright() as playwright:
        main(playwright)
