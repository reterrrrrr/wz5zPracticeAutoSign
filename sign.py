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
        self.read_env()
        self.program_cli()
        self.auto_renew()
        self.run()

    def getInfoByDingUserId(self, ding_user_id):
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19A348 AliApp(DingTalk/6.3.7) com.laiwang.DingTalk/21728861 Channel/201200 language/en-CN UT4Aplus/0.0.6 WK'
        header = {
            'DingTalk-Flag': '1',
            'User-Agent': ua
        }
        cookie = {'ding_userid': ding_user_id}
        print('[+]start to get other info')

        def get_recoed_id():
            url = 'http://218.75.25.135:81/dingPracticeApply.do?method=getPracticeApplyList&str1=&num1=1&num2=100'
            # {"records": [{"userName": "***", "userCode": "***", "recordId": ***, "companyName": "***", "reason": "***", "flagStr": "***"}],"count":1,"statusCode": 200}
            with httpx.Client() as client:
                req = client.get(url, headers=header, cookies=cookie)
                recordid = json.loads(req.text)['records'][0]['recordId']
            return recordid

        def getInfoByRecordId():
            url = 'http://218.75.25.135:81/dingPracticeApply.do?method=editPracticeApply&id={}&view=1'.format(
                get_recoed_id())
            with httpx.Client() as client:
                req = client.get(url, headers=header, cookies=cookie)
                return req.text

        def findInfoFromHtml():
            sel = Selector(getInfoByRecordId())
            lng = sel.css('#lng::attr(value)').get()
            lat = sel.css('#lat::attr(value)').get()
            companyid = sel.css('#i1::attr(value)').get()
            str5 = sel.css('#bdate::attr(value)').get()
            # i2 = sel.css('#i2::attr(value)').get()
            self.config += [
                {
                    "ding_id": ding_user_id,
                    "lng": lng,
                    "lat": lat,
                    "companyId": companyid,
                    "random": True,
                    "max_delay": 900,
                    "str5": str5,
                    "ua": ua
                }
            ]
        findInfoFromHtml()

    def program_cli(self):
        if not self.config:
            parser = argparse.ArgumentParser(description='')
            parser.add_argument('-c', '--conf', type=str,
                                help='conf file path')
            parser.add_argument('-C', '--confData', type=str, help='conf data')
            parser.add_argument('-d', '--dinguserid',
                                type=str, help='dinguserid')
            args = parser.parse_args()
            if args.conf:
                self.read_conf(args.conf)
            if args.confData:
                self.config == json.loads(args.confData)
            if args.dinguserid:
                for i in args.dinguserid.split(','):
                    print(i)
                    self.getInfoByDingUserId(i)

    def read_conf(self, path):
        with open(path, 'r') as f:
            self.config = json.loads(f.read())

    def push_function_bark(self, push_data):
        if self.barkid != '':
            res = httpx.get(
                'https://api.day.app/%s/%s?level=timeSensitive' % (self.barkid,push_data))
            return res
        else:
            return None

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
                        res = self.push_function_bark(
                            'server dns is error'
                        )

                except:
                    res = self.push_function_bark(
                        'sign faile\nserver is offline'
                    )
                    if res.status_code == 200:
                        print('server offline\npush done')
                        sys.exit(0)

    def read_env(self):
        try:
            self.config = json.loads(os.getenv('ENV_CONFIG'))
        except TypeError:
            self.config = []
        try:
            dinguserid = os.getenv('ENV_DINGUSERID')
            print(dinguserid)
            for i in dinguserid.split(','):
                self.getInfoByDingUserId(i)
        except:
            if self.config:
                pass
            else:
                self.config = []
        try:
            self.barkid = os.getenv('ENV_BARKID')
        except:
            self.barkid = ''

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

        postData = {
            'method': 'addPracticeCheck',
            'lng': lng,
            'lat': lat,
            'companyId': companyId,
            'str1': '|',
            'str5': str5
        }
        self.push_function_bark('[*]sign '+ding_userid+' start sign')

        if _random:
            delay = random.randint(0, max_delay)
            print(delay)
            await asyncio.sleep(delay)

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
