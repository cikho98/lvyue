import requests
import random
import os
import json
from seleniumwire import webdriver  # Import from seleniumwire
# from selenium import webdriver





class SpiderSina:
    def __init__(self):
        self.BASE = "https://weibo.com"
        headersnum = random.randint(0, 4)
        headerlist = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
        ]
        self.headers = {}
        self.headers["user-agent"] = headerlist[headersnum]

    # 爬取头像
    def spiderSina(self, i):
        dynamic_path = "/ajax/feed/hottimeline"
        par = "?since_id=0&refresh={}&group_id=1028032288&containerid=102803_ctg1_2288_-_ctg1_2288&extparam=discover%7Cnew_feed&max_id=0&count=10"
        dynamic_url = self.BASE + dynamic_path + par.format(i)
        re = requests.get(url=dynamic_url, headers=self.headers).json()
        statuses = re["statuses"]
        for j in range(0, len(statuses)):
            # 名称
            # statuses[1].user.screen_name
            screen_name = statuses[j]["user"]["screen_name"]
            # 高清头像
            # statuses[1].user.avatar_hd
            avatar_hd = statuses[j]["user"]["avatar_hd"]
            # 个人详情id
            # statuses[1].user.id
            uid = statuses[j]["user"]["id"]
            print("\n\n获取个人信息", re["ok"], screen_name, uid, "-------------")

<<<<<<< HEAD
            try:
                os.mkdir("./path/" + str(uid))
                os.mkdir("./path/" + str(uid) + "/headephoto")
                os.mkdir("./path/" + str(uid) + "/dynamic")
            except Exception as err:
                print(err)
            # 写入获取的数据格式json
            with open("./path/页面" + str(i) + ".js", "w+") as f:
                f.write(json.dumps(re))
            # 下载头像
            heade = requests.get(avatar_hd)
            with open("./path/" + str(uid) + "/headephoto/" + str(uid) + ".jpg", "wb") as a:
                a.write(heade.content)
                print("下载头像成功")
            # https://weibo.com/ajax/statuses/mymblog?uid=7055099262&page=1&feature=0
            profile_path = "/ajax/statuses/mymblog"
            par = "?uid={}&page=1&feature=0"
            profile_url = self.BASE + profile_path + par.format(uid)
            self.spiderDynamic(uid,profile_url)

    # 爬取个人信息动态前一页
    def spiderDynamic(self, uid, profile_url):
        self.headers[
            "cookie"] = "SUB=_2AkMVQ5b2f8NxqwJRmfgVy2njaYt-ywHEieKjH2ctJRMxHRl-yT8Xql0OtRB6PsO4GXRWdUjqnqe7PCZHUJbNtMYxRqre; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF37zSGXUl4odEWSBrB_q2z; SINAGLOBAL=9004044209628.855.1646205392474; ULV=1646205392555:1:1:1:9004044209628.855.1646205392474:; XSRF-TOKEN=5u680fnRvE8dGW6O2-0rVmVs; WBPSESS=yr8Ogb3qBlrorv2L6-ukSjrnUfaur8LpE8mb-kS1x90zOtxKCv0Sq66NqMu8FzeONSb_5CKk8-ZfOF_einAcUSUFwc-Mp0qjRQr9BZDOH1TYY7uvkDjgckUfWg1wsRd0OjM8WFTpzuobn3ywdZCu8t1IdPWk2BwrhoK2g5MjVNk="
        re = requests.get(profile_url, headers=self.headers).json()
        with open("./path/" + str(uid) + "/dynamic/用户动态详情第一页.js", "w+", encoding='UTF-8') as g:
            g.write(json.dumps(re))
        data = re["data"]["list"]
        # 第一层是朋友圈内容
        for i in range(0, len(data)):
            # 正文标题
            # data.list[0].text
            # data.list[3].text_raw
            text = data[i]["text_raw"]
            # 动态图片
            # data.list[0].pic_infos["006UuP9ply1gw9d1xhieoj30ui0u07cr"].largest.url
            # 获取动态图片
            try:
                pic_infos = data[i]["pic_infos"]
                pic_infos_keys = list(pic_infos.keys())
            except:
                pic_infos = []
            # 文件动态文件夹
            try:
                os.mkdir("./path/" + str(uid) + "/dynamic/" + str(i))
            except Exception as err:
                print(err)
            # 写入标题
            with open("./path/" + str(uid) + "/dynamic/" + str(i) + "/i.txt", "w+", encoding='utf-8') as title:
                title.write(text)
                print(text, "写入成功,准备下载图片:")
            # 第二层是图片
            if len(pic_infos) > 0:
                for j in range(0, len(pic_infos)):
                    try:
                        dynamicPhoto_url = pic_infos[pic_infos_keys[j]]["largest"]["url"]
                        dynamicPhoto = requests.get(dynamicPhoto_url)
                        with open("./path/" + str(uid) + "/dynamic/" + str(i) + "/" + str(j) + ".jpg", "wb") as dymaic:
                            dymaic.write(dynamicPhoto.content)
                            print("第%s张图片写入成功" % j)
                    except:
                        continue


def main():
    print("-" * 10 + "开始爬取sina微博" + "-" * 10)
    for i in range(1, 12):
        ss = SpiderSina()
        uid, profile_url = ss.spiderSina(i)

main()
=======
        # try:
        #     os.mkdir("/path")
        # except Exception as err:
        #     print(err)
        try:
            os.mkdir("./path/"+str(uid))
            os.mkdir("./path/"+str(uid)+"/headephoto")
            os.mkdir("./path/"+str(uid)+"/dynamic")
        except Exception as err:
            print(err)
        # 写入获取的数据格式json
        with open("./path/页面"+str(i)+".js","w+") as f:
            f.write(json.dumps(re))
        # 下载头像
        heade=requests.get(avatar_hd)
        with open("./path/"+str(uid)+"/headephoto/"+str(uid)+".jpg","wb") as a:
            a.write(heade.content)
        # https://weibo.com/ajax/statuses/mymblog?uid=2263026375&page=1&feature=0
        # https://weibo.com/ajax/statuses/mymblog?uid=7055099262&page=1&feature=0
        profile_path="/ajax/statuses/mymblog"
        par="?uid={}&page=1&feature=0"
        profile_url=self.BASE+profile_path+par.format(uid)
        self.spiderDynamic(profile_url)

    # 爬取个人信息动态前一页
    def spiderDynamic(self,profile_url):
        self.headers["cookie"]="SUB=_2AkMVQ5b2f8NxqwJRmfgVy2njaYt-ywHEieKjH2ctJRMxHRl-yT8Xql0OtRB6PsO4GXRWdUjqnqe7PCZHUJbNtMYxRqre; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF37zSGXUl4odEWSBrB_q2z; SINAGLOBAL=9004044209628.855.1646205392474; ULV=1646205392555:1:1:1:9004044209628.855.1646205392474:; XSRF-TOKEN=5u680fnRvE8dGW6O2-0rVmVs; WBPSESS=yr8Ogb3qBlrorv2L6-ukSjrnUfaur8LpE8mb-kS1x90zOtxKCv0Sq66NqMu8FzeONSb_5CKk8-ZfOF_einAcUSUFwc-Mp0qjRQr9BZDOH1TYY7uvkDjgckUfWg1wsRd0OjM8WFTpzuobn3ywdZCu8t1IdPWk2BwrhoK2g5MjVNk="
        re=requests.get(profile_url,headers=self.headers)
        print(re.text)
        # with open("./path/"+str(uid)+"/dynamic/用户动态详情第一页.js","w+") as g:
        #     g.write(json.dumps(re))
        # list=re["data"]["list"]
        # # 第一层是朋友圈内容
        # for i in range(0,len(list)):
        #     # 正文标题
        #     # data.list[0].text
        #     text=data[i]["text"]
        #     # 动态图片
        #     # data.list[0].pic_infos["006UuP9ply1gw9d1xhieoj30ui0u07cr"].largest.url
        #     pic_infos=list[i]["pic_infos"]
        #     try:
        #         os.mkdir("./path/"+str(uid)+"/dynamic/"+i)
        #     except Exception as err:
        #         print(err)
        #     with open("./path/"+str(uid)+"/dynamic"+str(i)+"i.txt","w+") as title:
        #         title.write(text)
        #     # 第二层是图片
        #     for j in range(0, len(pic_infos)):
        #         dynamicPhoto_url=pic_infos[j]["largest"]["url"]
        #         dynamicPhoto=requests.get(dynamicPhoto_url)
        #         with open("./path/"+str(uid)+"/dynamic"+str(i)+str(j)+".jpg","wb") as dymaic:
        #             dymaic.write(dynamicPhoto.content)


    def driver_chrome(self):

        # Create a new instance of the Chrome driver
        path=r"F:\python3.7\Lib\site-packages\seleniumwire\undetected_chromedriver\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path)

        # Go to the Google home page
        driver.get('https://weibo.com/newlogin?tabtype=weibo&gid=1028032288&url=https%3A%2F%2Fweibo.com%2F')

        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response:
                print(
                    # request.url,
                    # request.response.status_code,
                    request.response.headers
        )

ss=SpiderSina()
# ss.spiderHeade()
url="https://weibo.com/ajax/statuses/mymblog?uid=2030348253&page=1&feature=0"
# ss.spiderDynamic(url)
ss.driver_chrome()
>>>>>>> 11e954985f6b379b9b05133ac6b197704a853305
