# -*- coding:utf-8 -*-

import asyncio
import sys
import httpx
import random
import os
import json
import argparse
from parsel import Selector
import datetime


class AutoSign():

    def __init__(self) -> None:
        super().__init__()
        self.check_domain()
        self.sign_url = self.domain+'/dingPractice.do'
        self.renew_url = self.domain + '/dingCompanyRuleUser.do'
        sign.auto_renew()
        self.read_env()
        self.program_cli()

    def program_cli(self):
        if not self.config:
            parser = argparse.ArgumentParser(description='')
            parser.add_argument('-c', '--conf', type=str,
                                help='conf file path')
            parser.add_argument('-C', '--confData', type=str, help='conf data')
            args = parser.parse_args()
            if args.conf:
                self.read_conf(args.conf)
            if args.confData:
                self.config == json.loads(args.confData)

    def read_conf(self, path):
        with open(path, 'r') as f:
            self.config = json.loads(f.read())

    def push_function_bark(self, push_data):
        res = httpx.get(
            'https://api.day.app/vAGNHw7EDXTu93JbmK3PDJ/%s?level=timeSensitive' % push_data)
        return res

    def check_domain(self):
        with httpx.Client() as client:
            try:
                res = client.get('http://www.wz5z.com:81')
                if res.status_code == 200:
                    self.domain = 'http://www.wz5z.com:81'

            except:
                try:
                    res = client.get('http://218.75.25.135:81')
                    if res.status_code == 200:
                        self.domain = 'http://218.75.25.135:81'

                except:
                    res = self.push_function_bark(
                        'sign faile\nserver is offline')
                    if res.status_code == 200:
                        print('server offline\npush done')
                        sys.exit(0)

    def read_env(self):
        self.config = json.loads(os.getenv('ENV_CONFIG'))

    def auto_renew(self):
        for i in self.config:
            ding_userid = i['ding_id']
            ua = i['ua']
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

    async def sign(self, user_data):
        ding_userid = user_data['ding_id']
        lng = user_data['lng']
        lat = user_data['lat']
        companyId = user_data['companyId']
        _random = user_data['random']
        max_delay = user_data['max_delay']
        str5 = user_data['str5']
        ua = user_data['ua']
        header = {
            'DingTalk-Flag': '1',
            'User-Agent': ua
        }

        if _random:
            delay = random.randint(0, max_delay)
            print(delay)
            await asyncio.sleep(delay)

        postData = {
            'method': 'addPracticeCheck',
            'lng': lng,
            'lat': lat,
            'companyId': companyId,
            'str1': '|',
            'str5': str5
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.sign_url, headers=header, data=postData, cookies={'ding_userid': ding_userid})
            if res.status_code == 200:
                print('[*]sign '+ding_userid, res.text)
                self.push_function_bark('[*]sign '+ding_userid+' '+res.text)

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for i in self.config:
            tasks.append(self.sign(i))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


sign = AutoSign()
sign.run()
