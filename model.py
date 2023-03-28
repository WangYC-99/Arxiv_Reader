import openai
import requests
import json
import urllib.parse
import re
import hashlib
import random

info_f = open('config.json', 'r')
info = json.load(info_f)

class OpenAI():
    def __init__(self) :
        openai.api_key=info['openai_apikey']  # 这里填上购买的openai账号的密钥

    
    def generate_response_davinci(self, prompt):
        response = openai.Completion.create(
        model='code-davinci-002',  # 这里填上你此次需要的模型，这里我默认的是达芬奇3号
        prompt=prompt,
        temperature=0.7, # 控制随机性。控制响应的随机性，表示为从0到1的范围。默认0.7
        max_tokens=2048,  # 在完成时包含多少文本的限制
        top_p=0.8, # # 控制模型应考虑完成多少随机结果，如温度所建议的那样；它决定了随机性的范围。
        frequency_penalty=0,# 降低了模型通过“惩罚”它逐字重复同一行的可能性。
        presence_penalty=0 # 增加了它谈论新话题的可能性。
        )
        return response.choices[0].text.strip()

    def generate_response_chatgpt(self, messages):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', 
            messages=messages
        )
        result = response.choices[0].message.content
        return result
    
class Baidu():
    def __init__(self) -> None:
        self.app_id = info['baidu']['app_id']
        self.key = info['baidu']['app_key']
        self.salt = '2023'
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

    def md5(self, string):
        var = hashlib.md5()
        var.update(string.encode("utf-8"))
        return (var.hexdigest()).lower()

    def translate(self, query):
        sign = self.app_id + query + self.salt + self.key
        print(self.app_id)
        json_content = json.dumps({
            "q" : query,
            'from' : 'en',
            'to' : 'zh',
            'appid' : self.app_id,
            'salt' : self.salt,
            'sign' : self.md5(sign)
        })
        print(self.md5(sign))
        response = requests.post(
            url = self.url,
            headers = self.headers,
            data = json_content
        )
        result = response.json()
        return result

class BaiDuFanyi:
    def __init__(self):
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.fromLang = 'auto'
        self.toLang = 'zh'
        self.salt = random.randint(32768,65536)
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.appid = info['baidu']['app_id'] 
        self.secretKey = info['baidu']['app_key'] 

    def BdTrans(self,text):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign =md.hexdigest()
        data = {
            "appid": self.appid,
            "q": text,
            "from": self.fromLang,
            "to": self.toLang,
            "salt": self.salt,
            "sign": sign
        }
        response = requests.post(self.url, params= data, headers= self.header)  # 发送post请求
        text = response.json()  # 返回的为json格式用json接收数据
        results = text['trans_result'][0]['dst']
        return results