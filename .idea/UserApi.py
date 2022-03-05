from lvyuesiagn import make_sign
from lvyuesiagn import makepar
from SelectInfo import mysql
from database import databaseOperated
import requests
from qiniu import Auth, put_file, etag
import qiniu.config
import os
import shutil
import ssl
import urllib.parse
from PIL import Image




class UserApi:
    def __init__(self,mobileno):
        self.MOBILENO=mobileno
        self.BASE="http://lvyue.caichengwang.com"
        self.LAST="?appName=lvyue&appVersion=1.0.0&os=iOS"
        self.HEADERS={
            "User-Agent": "XBD/1.0.0 (iPhone; iOS 14.6; Scale/3.00)",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Content-Length": "290",
            "Connection": "keep-alive"
        }
        self.login()

    # 登录
    def login(self):
        data= {
            "appVersion":"1.0.0",
            "os": "android",
            "smsCode": "11223",
            "phone": "%s"%self.MOBILENO
        }
        par=makepar(data)
        url=self.BASE+"/acc/phone/login"+"?%s"%par
        self.HEADERS["sn"]=make_sign(data)
        re=requests.post(url,par,headers=self.HEADERS).json()
        self.access_token=re["data"]["access_token"]
        self.netEaseToken=re["data"]["netEaseToken"]
        self.uid=re["data"]["uid"]
        self.refresh_token=re["data"]["refresh_token"]
        self.jti=re["data"]["jti"]
        self.openId=re["data"]["openId"]
        self.unionId=re["data"]["unionId"]
        self.getTicket()

    # 获取ticket值
    def getTicket(self):
        url=self.BASE+"/oauth/ticket"+self.LAST
        par={'access_token': '%s'%self.access_token,
             'commonUserId': '%s'%self.uid,
             'ispType': '2'}
        self.HEADERS["sn"]=make_sign(par)
        re=requests.post(url,par,headers=self.HEADERS).json()
        self.ticket=re["data"]["tickets"][0]["ticket"]

    # 更新用户信息
    def uplogUserInfo(self,headeurl):
        # http%3A//qiniu.caichengwang.com/FuKMJaJ5YllBs93aHMjK9y_5VocK?imageslim?
        url =self.BASE+"/user/v2/update"+self.LAST
        par={
            'avatar': '%s'%headeurl,
            'commonUserId': '%s'%self.uid,
            'ticket': "%s"%self.ticket,
            # 'ticket': "a57d2828460ea9f94efc093428baf4aa",
            'uid': '%s'%self.uid
            }
        sn=make_sign(par,self.ticket)
        self.HEADERS["sn"]=sn
        response = requests.request("POST", url, headers=self.HEADERS, data=par).json()
        print("更新信息，%s"%response["code"])
        # print(response)


class UpdateQiniu:
    def __init__(self):
        self.access_key="vyT3O_cD_P-oBrOowstxpwqIv6mHoIBnlhiieMTU"
        self.secret_key="Q375PcEHWQSc6akQPC54waFsqvhLIP53RHsu9yAY"
        #要上传的空间
        self.bucket_name='cikho98'
        # 域名
        self.base_url="http://r81k5uvur.hn-bkt.clouddn.com/"
        self.local_paths=r"C:\Users\cc-ccw\Desktop\cctest\test"

    # 查询用户信息
    def selectUserInfo(self):
        info=mysql("lvyue","select * from lvyueuserinfo")
        return info

    # 更新到七牛
    def uplogQiniu(self,key,localfile):
        access_key=self.access_key
        secret_key=self.secret_key
        q = Auth(access_key, secret_key)
        #要上传的空间
        bucket_name = self.bucket_name
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        localfile = r"%s"%localfile
        ret, info = put_file(token, key, localfile, version='v2')
        paths=ret["key"]
        # assert ret['key'] == key
        # assert ret['hash'] == etag(localfile)
        return self.base_url+paths

    # 打开文件夹
    def openPhotoFile(self):
        result=os.listdir(self.local_paths)
        return result

    # 更新图片名字（可不理）
    def updatePhotoName(self,info,result):
        for i in range(0,len(info)):
            os.rename(self.local_paths+'\\'+str(result[i]),self.local_paths+'\\'+str(info[i]["lvyueNum"])+".jpg")

    # 创建用户userfile
    def createUserFile(self,info):
        for i in range(0,len(info)):
            # os.mkdir(self.local_paths+"\\"+str(info[i]["lvyueNum"]))
            os.mkdir(self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\headephoto")
            os.mkdir(self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\dynamic")
    
    # 移动头像，可不理
    def movePhoto(self,info):
        for i in range(0,len(info)):
            oldpath=self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\"+str(info[i]["lvyueNum"])+".jpg"
            newpath=self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\headephoto\\"+str(info[i]["lvyueNum"])+".jpg"
            shutil.move(oldpath,newpath)

    # 获取头像路径
    def getHeadPhotoPaths(self,lvyueNum):
        result=os.listdir(self.local_paths+"\\"+str(lvyueNum)+"\\headephoto\\cutHeadePhoto")
        headePaths=[]
        for i in range(0,len(result)):
            headePath=self.local_paths+"\\"+str(lvyueNum)+"\\headephoto\\cutHeadePhoto"+'\\'+str(result[i])
            headePaths.append(headePath)
        return headePaths

    # 截取头像路径
    def cutHeadePhoto(self,info):
        for i in range(0,len(info)):
            img = Image.open(self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\headephoto\\"+str(info[i]["lvyueNum"])+".jpg")
            w,h=img.size
            l=int((int(w)/2)-270)
            t=int((int(h)/2)-270)
            r=int((int(w)/2)+270)
            d=int((int(h)/2)+270)
            if l<0:
                l=0
                r=w
            if t<0:
                t=0
                d=h
            # print(w,h)
            # print(l,t,r,d)
            cropped = img.crop((l,t,r,d))# (left, upper, right, lower)
            # Image._show(cropped)
            try:
                os.mkdir(self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\headephoto\\"+"cutHeadePhoto")
            except OSError as error:
                print(error)
            cropped.save(self.local_paths+"\\"+str(info[i]["lvyueNum"])+"\\headephoto\\"+"cutHeadePhoto"+'\\'+str(info[i]["lvyueNum"])+"_cut.jpg")

    # 数据库更新头像图片路径
    def update_headPhotoPaths(self,lvyueNum):
        filepaths=self.getHeadPhotoPaths(lvyueNum)
        for i in range(0,len(filepaths)):
            filepath=filepaths[i].replace("\\","/")
            # UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
            # mysql("lvyue","insert into lvyueuserinfo set headeurl=%s where lvyueNum=%s"%(filepaths,lvyueNum))
            updatesql="update lvyueuserinfo set headepath=\"%s\" where lvyueNum=%s;"%(filepath,lvyueNum)
            databaseOperated("lvyue",updatesql)

    # 数据库更新头像地址
    def update_headPhotoUrl(self,lvyueNum,url):
        # UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
        # mysql("lvyue","insert into lvyueuserinfo set headeurl=%s where lvyueNum=%s"%(filepaths,lvyueNum))
        updatesql="update lvyueuserinfo set headeurl=\"%s\" where lvyueNum=%s;"%(url,lvyueNum)
        databaseOperated("lvyue",updatesql)




uq=UpdateQiniu()
result=uq.openPhotoFile()
# 更新图片名字
# uq.updatePhotoName(info,result)
# 创建吕悦号文件夹
# uq.createUserFile(info)
# 移动头像
# uq.movePhoto(info)
# 获取头像路径
# uq.getHeadPhotoPaths(info[0]["lvyueNum"])
# 截取头像
# uq.cutHeadePhoto(info)
info=uq.selectUserInfo()
for i in range(0,len(info)):
    mobileno=info[i]["phone"]
    ua=UserApi(mobileno)
    lvyueNum=info[i]["lvyueNum"]
    # # # localfile=info[i]["headepath"]
    # # # 数据库更新头像图片路径
    # # uq.update_headPhotoPaths(lvyueNum)
    # path=uq.getHeadPhotoPaths(lvyueNum)[0]
    # # 上传7牛
    # url=uq.uplogQiniu(str(lvyueNum)+"_cut",path)
    # uq.update_headPhotoUrl(info[i]["lvyueNum"],url)
    # info=uq.selectUserInfo()
    # #app更新用户信息
    headeurl=info[i]["headeurl"]
    ua.uplogUserInfo(headeurl)

