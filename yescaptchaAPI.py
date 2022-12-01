"""
author: Zakkoree
"""
import time
import requests
from commonlog import Logger

logger = Logger(LoggerName="yescaptchaAPI")

def create_task(clientKey: str, websiteKey: str, websiteURL: str) -> str:
    data = {
        "clientKey": clientKey,
        "task": {
            "websiteURL": websiteURL,
            "websiteKey": websiteKey,
            "type": "NoCaptchaTaskProxyless"
        }
    }
    return create(data)

def create(data):
    try:
        url = "https://api.yescaptcha.com/createTask"
        requests.packages.urllib3.disable_warnings()
        return requests.post(url, json=data, verify=False).json()
    except Exception as e:
        logger.error(e)
        return None


def create_task_v3(clientKey: str, websiteKey: str, websiteURL: str, pageAction: str) -> str:
    data = {
        "clientKey": clientKey,
        "task": {
            "websiteURL": websiteURL,
            "websiteKey": websiteKey,
            "pageAction" : pageAction,
            "type": "RecaptchaV3TaskProxyless"
        }
    }
    return create(data)


def get_response(taskID: str, clientKey: str):
    times = 0
    while times < 60:
        try:
            url = f"https://api.yescaptcha.com/getTaskResult"
            data = {
                "clientKey": clientKey,
                "taskId": taskID
            }
            requests.packages.urllib3.disable_warnings()
            result = requests.post(url, json=data, verify=False).json()
            solution = result.get('solution', {})
            if solution:
                response = solution.get('gRecaptchaResponse')
                if response:
                    return response
            if result.get('errorId') == 1:
                return None
        except Exception as e:
            logger.error(e)

        times += 3
        time.sleep(3)
    logger.error("yescaptcha get_response timeout")
    return None

        

def verify_website(response, websiteURL):
    data = {"g-recaptcha-response": response}
    r = requests.post(websiteURL, data=data)
    if r.status_code == 200:
        return r.text
        
        
def asr(clientKey: str, websiteKey: str, websiteURL: str, task_type: str):
    taskResult = create_task(clientKey, websiteKey, websiteURL, task_type)
    taskId = taskResult.get('taskId')
    if taskId is not None:
        response = get_response(taskId, clientKey)
        logger.info("yescaptcha :" + response)
        return response
        # result = verify_website(response)
        # print('验证结果：', result)
    else:
        logger.error("yescaptcha create_task :" + taskResult.get('errorDescription'))
        return None

def asrV3(clientKey: str, websiteKey: str, websiteURL: str, pageAction: str):
    taskResult = create_task_v3(clientKey, websiteKey, websiteURL, pageAction)
    taskId = taskResult.get('taskId')
    if taskId is not None:
        response = get_response(taskId, clientKey)
        logger.info("yescaptcha V3 :" + response)
        return response
        # result = verify_website(response, websiteURL)
        # print('验证结果：', result)
    else:
        logger.error("yescaptcha V3 create_task :" + taskResult.get('errorDescription'))
        return None

if __name__ == '__main__':
    # clientKey：在个人中心获取
    clientKey = "xxxxxxxx"
    # 目标参数：
    websiteKey = "6LdZ3_YZAAAAALyzLQjyjE6RPFdcG9A-TLr6AxF0"
    # 目标参数：
    websiteURL = "https://woiden.id"
    asr(clientKey, websiteKey, websiteURL)