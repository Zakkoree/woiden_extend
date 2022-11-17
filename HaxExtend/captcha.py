import os
import time
import json
import urllib
import sys
import ffmpy3
import globalVal
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from aip import AipSpeech
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
from commonlog import Logger
import main

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

delayTime = 2
audioToTextDelay = 10
TWOCAPTCHA_TOKEN = os.environ['TWOCAPTCHA_TOKEN']
solver = TwoCaptcha(TWOCAPTCHA_TOKEN)

logger = Logger(LoggerName = "HaxExtend")

def recaptchaV3():
#     return True
    logger.info("verify recaptcha v3")
#     print("[INFO] verify recaptcha v3")
    # https://woiden.id/dist/js/renew-vps.js
    chaper_url = 'https://' + main.origin_host + main.google_recaptchaV3_js_path
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
    req = Request(url=chaper_url, headers=headers) 
    html = urlopen(req)
    bs = str(BeautifulSoup(html, 'html.parser'))
    # for link in bs.find_all('a'):
    #     if 'href' in link.attrs:
    #         print(link.attrs['href'])

    actionIndex = bs.find("action:")
    sitekeyStart = bs.find("execute(") + 9
    sitekeyEnd = actionIndex - 3
    sitekey = bs[sitekeyStart : sitekeyEnd]
    logger.info("sitekey:" + sitekey)
#     print("[INFO] sitekey:", sitekey)
    actionStart = actionIndex + 8
    actionEnd = bs.find("}).then(") -1
    action = bs[actionStart : actionEnd]
    logger.info("action:" + action)
#     print("[INFO] action:", action)

    # api_key = os.getenv('APIKEY_2CAPTCHA', TWOCAPTCHA_TOKEN)
    # solver = TwoCaptcha(api_key)
    # https://woiden.id/vps-renew/
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url='https://' + main.origin_host + main.renew_path,
            version='v3',
            action=action,
            score=0.9
        )

    except Exception as e:
        logger.error("recaptchaV3 Service Exception")
        logger.error(e)
#         print("[ERROR] recaptchaV3 Service Exception")
#         print("[ERROR] " + str(e))
        return ""

    else:
        logger.info("solved:" + str(result))
#         print('[INFO] solved: ' + str(result))
        # 一旦我们有了令牌，我们就可以执行在方法调用中引用的相同代码， .then() 并将我们的令牌作为函数调用参数传递。在我们的演示案例中，我们可以在javascript控制台中打开javacsript执行以下代码：
        # window.verifyRecaptcha('03AGdBq27lvCYmKkaqDdxWLfMe3****')
#         javacsript = "window.verifyRecaptcha('" + result['code'] + "')"
#         globalVal.driver.execute_script(javacsript)

        globalVal.driver.switch_to.default_content()
        recaptchaFound = False
        iframes = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')
        for index in range(len(iframes)):
            globalVal.driver.switch_to.default_content()
            iframe = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')[index]
            globalVal.driver.switch_to.frame(iframe)
            globalVal.driver.implicitly_wait(delayTime)
            try:
                globalVal.driver.find_element(By.ID, "recaptcha-token")
                javacsript = """document.getElementById('recaptcha-token').value='{token}'""".replace("{token}",  result['code'])
                globalVal.driver.execute_script(javacsript)
                recaptchaFound = True
                logger.info("token done")
                break
            except Exception as e:
                pass

#         javacsript = """$("button[name='submit_button']").unbind('click').click(function(){$('#form-submit').prepend('<input type="hidden" name="token" value="{token}">');$('#form-submit').prepend('<input type="hidden" name="action" value="renew_vps">');$("html, body").animate({scrollTop:300},"slow");$("#response").html('<div class="progress" id="progress"><div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 10%"><span class="sr-only">Loading.....</span></div></div>'),$(".progress-bar").animate({ width:"25%"}),$(".progress-bar").animate({width:"55%"}),$.ajax({ type:"POST",url:"/renew-vps-process/",data: $("form.submit").serialize(),success:function (a) {$(".progress-bar").animate({ width:"70%"}),$(".progress-bar").animate({width:"100%"}),$("#response").html(a),$("#form-submit").hide(1000)},error:function(){alert("Something wrong !")}})})""".replace("{token}",  result['code'])
#         javacsript = """document.getElementById('recaptcha-token').value='{token}'""".replace("{token}",  result['code'])
#         javacsript = bs.replace("'+token+'", result['code'])
#         globalVal.driver.execute_script(javacsript)
        
#         globalVal.driver.execute_script(
#         """document.querySelector('[name="g-recaptcha-response-100000"]').innerText='{}'""".format(result['code']))

        globalVal.driver.switch_to.default_content()
        return result['code']


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def mp3_change_pcm(audioFile):
    logger.info("Audio frequency transcoding")
#     print("[INFO] Audio frequency transcoding")
    outpath = os.getcwd() + "audio.pcm"
    ff = ffmpy3.FFmpeg(
        inputs={audioFile: '-y'},
        outputs={
            outpath.format(audioFile): '-acodec pcm_s16le -f s16le -ac 1 -ar 16000'}
    )
    ff.run()
    return outpath

def audioToText(audioFile):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    jsonResult = client.asr(get_file_content(mp3_change_pcm(audioFile)), 'pcm', 16000, {
        'dev_pid': 1737,
    })
    result = jsonResult['result'][0]
#     print("[INFO] Audio verify code:" + str(jsonResult))
    logger.info("udio verify code:" + str(jsonResult))
    return result

def twoCaptcha():
    # google大概率不会让你用音频，只能用图片
    g_recaptcha = globalVal.driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()
    sitekey = g_recaptcha.get_attribute("data-sitekey")
    result = solver.recaptcha(sitekey=sitekey, url='https://' + main.origin_host + main.login_path)
#     print("[INFO] recaptcha_res", result)
    logger.info("recaptcha_res" + str(result))
    globalVal.driver.execute_script(
        """document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(result['code']))
#     print('[INFO] reCAPTCHA picture done')
    logger.info("reCAPTCHA picture done")
    globalVal.driver.switch_to.default_content()
    return 1


def reCAPTCHA():
    g_recaptcha = globalVal.driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()
    
    iframes = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        globalVal.driver.switch_to.default_content()
        iframe = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')[index]
        globalVal.driver.switch_to.frame(iframe)
        globalVal.driver.implicitly_wait(delayTime)
        try:
            audioBtn = globalVal.driver.find_element(By.ID, "recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                time.sleep(2)
                # get the mp3 audio file
                src = globalVal.driver.find_element(By.ID, "audio-source").get_attribute("src")
#                 src = globalVal.driver.find_element(By.CLASS_NAME, "rc-audiochallenge-tdownload-link").get_attribute("href")
#                 print("[INFO] Audio src: %s" % src)
                logger.info("Audio src:" + str(src))
                outPath = os.getcwd() + "audio.mp3"
                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, outPath)

                # Speech To Text Conversion
                key = audioToText(outPath)
#                 print("[INFO] Recaptcha Key: %s" % key)
                logger.info("Recaptcha Key:" + str(key))

                globalVal.driver.switch_to.default_content()
                iframe = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                globalVal.driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = globalVal.driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                main.delay()
                inputField.send_keys(Keys.ENTER)
                main.delay()
                main.delay()

                err = globalVal.driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    logger.info("reCAPTCHA audio done")
#                     print('[INFO] reCAPTCHA audio done')
                    return 1

        except Exception as e:
            logger.error(e)
            logger.warn("Possibly blocked by google. Change IP,Use Proxy method for requests")
            logger.info("Audio verify fail,try picture fuck reCAPTCHA")
#             print("[ERROR] " + str(e))
#             print("[WARN] Possibly blocked by google. Change IP,Use Proxy method for requests")
#             print("[INFO] Audio verify fail,try picture fuck reCAPTCHA")
#             twoCaptcha(g_recaptcha)
            # sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
            return 2
    else:
        # sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
#         print('[ERROR] reCAPTCHA not found!')
        logger.error("reCAPTCHA not found!")
        return 3
    


def numCAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(
        globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][
            0])
    caculateMethod = globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(
        globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][
            0])
    
    if caculateMethod == '+':
        captcha_result = number1 + number2
    elif caculateMethod == '-':
        captcha_result = number1 - number2
    elif caculateMethod == 'X':
        captcha_result = number1 * number2
    elif caculateMethod == '/':
        captcha_result = number1 / number2
        
#     print('[INFO] renewal verify code:', number1, caculateMethod, number2, '=', captcha_result)
    logger.info("renewal verify code:"+ str(number1) + str(caculateMethod) + str(number2) + '=' + str(captcha_result))
    return captcha_result
