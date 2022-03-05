# encoding=utf-8

import hashlib
import json
# import datetime
import time


def make_sign(data,token=""):
    timeNow=str(time.time())
    data["t"]="%s"%timeNow
    md5 = hashlib.md5()
    # keyv = ["=".join(i) for i in data.items() if i[1] != "" and i[0] != "sign"]
    keyv = ["=".join(i) for i in data.items() if i[0] != "sign"]   # 返回list
    # keyv["t"]=
    # keyv=data.replace("&","")
    # keyv = "&".join(keyv)  # 每次字段间隔加入符号
    keyv = "".join(sorted(keyv))  # 升序排序
    dt = keyv + token
    md5.update(dt.encode(encoding='utf-8'))
    sign = md5.hexdigest()
    # else:
    #     # data=json.dumps(data,ensure_ascii=False)
    #     dt = json.dumps(data, ensure_ascii=False).replace(', ', ',') + cctoken
    #     # print(dt)
    #     md5 = hashlib.md5()
    #     md5.update(dt.encode('utf-8'))
    #     sign = md5.hexdigest()
    return sign[:7]

def makepar(data):
    keyv = ["=".join(i) for i in data.items() if i[0] != "sign"]   # 返回list
    keyv = "&".join(sorted(keyv))  # 升序排序
    return keyv

#
# par={
#     "appVersion":"1.0.0",
#     "os": "android",
#     "smsCode": "11223",
#     "phone": "17138879442"
# }
# # make_sign(par)
# makepar(par)