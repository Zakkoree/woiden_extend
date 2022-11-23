"""
author: Zakkoree
"""

import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
from commonlog import Logger
logger = Logger(LoggerName="tencent")

def asr(secretId, secretKey, url):
    # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
    # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
    cred = credential.Credential(secretId, secretKey)
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "asr.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = asr_client.AsrClient(cred, "", clientProfile)
    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.CreateRecTaskRequest()
    params = {
        "EngineModelType": "16k_en",
        "ChannelNum": 1,
        "ResTextFormat": 1,
        "SourceType": 0,
        "Url": url
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个CreateRecTaskResponse的实例，与请求对象对应
    resp = client.CreateRecTask(req)

    while True:
        qeq = models.DescribeTaskStatusRequest()
        params = {
            "TaskId": json.loads(resp.to_json_string())['Data']['TaskId']
        }
        qeq.from_json_string(json.dumps(params))
        
        # 返回的resp是一个DescribeTaskStatusResponse的实例，与请求对象对应
        qesp = client.DescribeTaskStatus(qeq)
        # 输出json格式的字符串回包
        if json.loads(qesp.to_json_string())['Data']['Status'] == 2:
            logger.info(qesp.to_json_string())
            return json.loads(qesp.to_json_string())['Data']['ResultDetail'][0]['SliceSentence']
        elif json.loads(qesp.to_json_string())['Data']['Status'] == 1 or json.loads(qesp.to_json_string())['Data']['Status'] == 0:
            time.sleep(1)
        else:
            logger.error(json.loads(qesp.to_json_string())['Data']['ErrorMsg'])
            return None
    
    

if __name__ == '__main__':
    asr("xxx", "xxx", "https://www.recaptcha.net/recaptcha/api2/payload?p=06AEkXODC67t6BYxAVzUmL_w8DLpR74kmcJXvl0folzoGA-cPxYlCWGOL_PNP5BYzX-qUM2GPRJLD8JEmnsKo1XN0nqoxWJ5YoTK5ozLChtT2SSWBCgQ6wZDwedE3g2-05iIm8b8h53S_WSsiGuWIwIHwG3St5ARCAXvaGi5QYWr6x8D8mkw5GBC9i2hUQfZp5Bp7_Fn_GZxgHNH-TkbfwiJX977PS_v3Uzw&k=6LdZ3_YZAAAAALyzLQjyjE6RPFdcG9A-TLr6AxF0")
