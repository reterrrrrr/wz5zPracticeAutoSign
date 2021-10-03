# -*- coding:utf-8 -*-

import httpx
import random
import os
import time

class AutoSign():

    def __init__(self) -> None:
        super().__init__()
        self.read_env()
        self.sign()
    def read_env(self):
        self.ding_userid = os.getenv('ENV_DINGID')
        self.lng = os.getenv('ENV_LNG')
        self.lat = os.getenv('ENV_LAT')
        self.companyId = os.getenv('ENV_COMPANYID')
        self._random = os.getenv('ENV_RANDOM')
        if self._random == None:
            self._random = True
        else:
            self.max_delay = os.getenv('ENV_MAX_DELAY')
            if not self.max_delay:
                self.max_delay = 900
        self.str5 = os.getenv('ENV_STR5')

    def sign(self):
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18H17 AliApp(DingTalk/6.0.31) com.laiwang.DingTalk/15216879 Channel/201200 language/zh-Hans-CN UT4Aplus/0.0.6 WK'
        header = {
            'DingTalk-Flag': '1',
            'User-Agent': ua
        }

        if self._random:
            delay = random.randint(0,self.max_delay)
            time.sleep(delay)

        postData = {
            'method': 'addPracticeCheck',
            'lng': self.lng,
            'lat': self.lat,
            'companyId': self.companyId,
            'str1': '|',
            'str5': self.str5
        }
            
        with httpx.Client() as client:
            res = client.post('http://www.wz5z.com:81/dingPractice.do',headers=header,data=postData,cookies={'ding_userid': self.ding_userid})
            if res.status_code == 200:
                pass

sign = AutoSign()
