import requests
import random
import os
import json

class SpiderSina:
    def __init__(self):
        self.BASE="https://weibo.com"
        headersnum=random.randint(0,4)
        headerlist=['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
                    ]
        self.headers ={}
        self.headers["user-agent"]=headerlist[headersnum]

    def spiderHeade(self):
        dynamic_path="/ajax/feed/hottimeline"
        par="?since_id=0&refresh={}&group_id=1028032288&containerid=102803_ctg1_2288_-_ctg1_2288&extparam=discover%7Cnew_feed&max_id=0&count=10"
        # for i in range(1,10):
        i=1
        dynamic_url=self.BASE+dynamic_path+par.format(i)
        re=requests.get(url=dynamic_url,headers=self.headers).json()
        statuses=re["statuses"]
        # 名称
        # statuses[1].user.screen_name
        screen_name=statuses[i]["user"]["screen_name"]
        # 高清头像
        # statuses[1].user.avatar_hd
        avatar_hd=statuses[i]["user"]["avatar_hd"]
        # 个人详情id
        # statuses[1].user.id
        uid=statuses[i]["user"]["id"]

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
        # 'https://weibo.com/ajax/statuses/mymblog?uid=2410655081&page=1&feature=0'
        profile_path="/ajax/statuses/mymblog"
        par="?uid={}&page=1&feature=0"
        profile_url=self.BASE+profile_path+par.format(uid)
        self.spiderDynamic(profile_url)

    # 爬取个人信息动态前一页
    def spiderDynamic(self,profile_url):
        print(profile_url)
        re=requests.get(profile_url,headers=self.headers).json()
        print(re)
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



ss=SpiderSina()
ss.spiderHeade()