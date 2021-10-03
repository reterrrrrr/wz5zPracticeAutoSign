# -*- coding:utf-8 -*-

import asyncio
import httpx
import random
import time


class AutoSign():
    def __init__(self,  name, ding_userid, lng, lat, companyId, str5, ua='Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18G82 AliApp(DingTalk/6.0.28) com.laiwang.DingTalk/15176062 Channel/201200 language/zh-Hans-CN UT4Aplus/0.0.6 WK') -> None:
        super.__init__()
        self.name = name
        # random delay time
        self.delay = random.randint(0, 1800)
        # set prosonal data
        self.ding_userid = ding_userid
        self.lng = lng
        self.lat = lat
        self.companyId = companyId
        self.str5 = str5
        self.ua = ua
        print(self.name, self.delay)

        self.header = {
            'DingTalk-Flag': '1',
            'User-Agent': self.ua
        }

    async def read_config_file(self):
        self.config = ''

    async def sign(self):
        postData = {
            'method': 'addPracticeCheck',
            'lng': self.lng,
            'lat': self.lat,
            'companyId': self.companyId,
            'str1': '|',
            'str5': self.str5
        }
        async with httpx.AsyncClient() as client:
            res = await client.post('http://www.wz5z.com:81/dingPractice.do',headers=header,data=postData)
            if res.status_code == 200:
                return res.text

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for i in self.tasks:
            tasks.append(i)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

sign = AutoSign()
sign.run()
