"""
author: Zakkoree
"""

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from commonlog import Logger

logger = Logger(LoggerName="ibmAPI")

def asr(IDkey, URL, audioFile):
    authenticator = IAMAuthenticator(IDkey)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(URL)

    with open(audioFile, 'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            # content_type='audio/flac',  # 指定转换的音频是.flac音频格式
            # content_type='audio/wav',  # 指定转换的音频是.wav音频格式
            content_type='audio/mp3',  # 指定转换的音频是.mp3音频格式
            # model='zh-CN_BroadbandModel',  # 表示识别中文语音，不指定则默认识别英文
            # timestamps=True  # 识别内容对应的时间轴（作字幕很重要的一个属性，但是我还不知道具体怎么使用）
        ).get_result()
    result = ""
    for i in speech_recognition_results['results']:
        for w in i['alternatives']:
            result += w['transcript']

    logger("audio result" + result)
    return result