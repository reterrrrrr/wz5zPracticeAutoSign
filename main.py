# -*- coding:utf-8 -*-

import asyncio
import httpx
import random
import os
import json
import time
import argparse



class AutoSign():

    def __init__(self) -> None:
        super().__init__()
        self.read_env()
        self.program_cli()

    def program_cli(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('-c','--conf',type=str,help='conf file path')
        parser.add_argument('-d','--ding-userid',type=str,help='dingid',required=True)
        parser.add_argument('-C','--companyId',type=str,help='companyId',required=True)
        parser.add_argument('-lng',type=str,help='lng',required=True)
        parser.add_argument('-lat',type=str,help='lat',required=True)
        parser.add_argument('-s','--str5',type=str,help='str5',required=True)
        parser.add_argument('-r','--random',type=bool,help='enable random delay',default=True)
        parser.add_argument('-m','--max-delay-time',type=int,help='enter max delay time sec',default=1800)
        args = parser.parse_args()
        if args.conf:
            self.read_conf(args.conf)

    def read_conf(self,path):
        with open(path,'r') as f:
            self.config = json.loads(f.read())
            
    def read_env(self):
        ding_userid = os.getenv('ENV_DING_USERID')
        companyId = os.getenv('ENV_COMPANYID')
        lng = os.getenv('ENV_LNG')
        lat = os.getenv('ENV_LAT')
        str5 = os.getenv('ENV_STR5')
        self.config = os.getenv('ENV_CONFIG')
        if self.config:
            self.config['dingid']['lng']['lat']['companyId']['random']['max_delay']['str5']['name']['ua'] = ding_userid,lng,lat,companyId,'','',str5,'','Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18G82 AliApp(DingTalk/6.0.28) com.laiwang.DingTalk/15176062 Channel/201200 language/zh-Hans-CN UT4Aplus/0.0.6 WK'

    async def sign(self,postData,header,ding_userid):
        async with httpx.AsyncClient() as client:
            res = await client.post('http://www.wz5z.com:81/dingPractice.do',headers=header,data=postData,cookies={'ding_userid': ding_userid})
            if res.status_code == 200:
                return res.text

    async def program(self):
        pass
    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        if self.config:
            for user in self.config:
                ding_userid = user['ding_id']
                lng = user['lng']
                lat = user['lat']
                companyId = user['companyId']
                _random = user['random']
                max_delay = user['max_delay']
                str5 = user['str5']
                name = user['name']
                ua = user['ua']
                header = {
                    'DingTalk-Flag': '1',
                    'User-Agent': ua
                }

                if _random:
                    delay = random.random(0,max_delay)
                    print(name,delay)
                    time.sleep(delay)

                postData = {
                    'method': 'addPracticeCheck',
                    'lng': lng,
                    'lat': lat,
                    'companyId': companyId,
                    'str1': '|',
                    'str5': str5
                }
                tasks.append(self.sign(postData=postData,header=header,ding_userid=ding_userid))

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

sign = AutoSign()
sign.run()
