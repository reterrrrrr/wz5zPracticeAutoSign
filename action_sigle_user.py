# -*- coding:utf-8 -*-

import httpx
import random
import os
import time
from parsel import Selector
import datetime
import json


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
        self.bark_id = os.getenv('ENV_BARKID')
        if self._random == None:
            self._random = True
        else:
            self.max_delay = os.getenv('ENV_MAX_DELAY')
            if not self.max_delay:
                self.max_delay = 900
        self.str5 = os.getenv('ENV_STR5')

    def sign(self):
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18H17 AliApp(DingTalk/6.0.31) com.laiwang.DingTalk/15216879 Channel/201200 language/zh-Hans-CN UT4Aplus/0.0.6 WK'
        header = {
            'DingTalk-Flag': '1',
            'User-Agent': self.ua
        }

        if self._random:
            delay = random.randint(0, self.max_delay)
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
            res = client.post('http://www.wz5z.com:81/dingPractice.do', headers=header,
                              data=postData, cookies={'ding_userid': self.ding_userid})
            if res.status_code == 200:
                pass

    def auto_renew(self):
        ding_userid = self.ding_userid
        ua = self.ua
        header = {
            'DingTalk-Flag': '1',
            'User-Agent': ua
        }
        with httpx.Client() as client:
            user_sign_time = client.get(self.renew_url +
                                        '?method=getCompanyRuleUserList&name=&num1=1&num2=100', headers=header, cookies={'ding_userid': ding_userid})
            json_data = json.loads(user_sign_time.text)
            if datetime.datetime.strptime(json_data['records'][0]['endDate'], r'%Y-%m-%d').__sub__(datetime.datetime.now()).days < 3:
                print('[*]renew '+ding_userid, 'start renew')
                self.push_function_bark('[*]renew ' +
                                        ding_userid+' start renew')
                item_num = 0
                while json_data['records'][item_num]['flagStr'] == '未审核':
                    item_num += 1

                get_time = client.get(self.renew_url +
                                        '?method=editCompanyRuleUser&id={}&view=1'.format(json_data['records'][item_num]['recordId']), headers=header, cookies={'ding_userid': ding_userid})
                selector = Selector(get_time.text)
                time_list = []
                for i in range(7, 21, 2):
                    time_list += [selector.css(
                        'input::attr(value)').getall()[i]]

                renew_data = {
                    'method': 'saveCompanyRuleUser',
                    'id': '0',
                    'beginDate': datetime.datetime.strftime(datetime.datetime.strptime(
                        json_data['records'][0]['endDate'], r'%Y-%m-%d')+datetime.timedelta(hours=24), r'%Y-%m-%d'),
                    'i1': '1',
                    'strs1': time_list
                }
                res = client.post(self.renew_url, headers=header,
                                    cookies={'ding_userid': ding_userid}, data=renew_data)
                self.push_function_bark('[*]renew ' +
                                        ding_userid+' '+res.text)
                print('[*]renew ' +
                        ding_userid+' '+res.text)

    def push_function_bark(self, push_data):
        res = httpx.get(
            'https://api.day.app/%s/%s?level=timeSensitive' % (self.bark_id,push_data))
        return res


sign = AutoSign()
