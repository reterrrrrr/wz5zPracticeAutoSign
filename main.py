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

    def read_env(self):
        self.config = json.loads(os.getenv('ENV_CONFIG'))

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
            time.sleep(delay)

        postData = {
            'method': 'addPracticeCheck',
            'lng': lng,
            'lat': lat,
            'companyId': companyId,
            'str1': '|',
            'str5': str5
        }

        async with httpx.AsyncClient() as client:
            res = await client.post('http://www.wz5z.com:81/dingPractice.do', headers=header, data=postData, cookies={'ding_userid': ding_userid})
            if res.status_code == 200:
                pass

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for i in self.config:
            tasks.append(self.sign(i))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


sign = AutoSign()
sign.run()
