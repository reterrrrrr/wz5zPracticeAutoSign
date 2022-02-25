import json
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
import socket
import httpx
from parsel import Selector
import time

def get_ding_id():
    class GetDingUserId:

        def request(self, flow):
            if flow.request.host == 'www.wz5z.com' and flow.request.port == 81:
                global ding_user_id
                ding_user_id = flow.request.cookies['ding_userid']
                m.shutdown()

    opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
    m = DumpMaster(options=opts, with_termlog=False, with_dumper=False)
    m.addons.add(GetDingUserId())
    print('[+]start proxy')
    print('[+]please set wlan proxy', 'Server:' +
          socket.gethostbyname(socket.gethostname()), 'Port:8080')
    m.run()
    print('[+]get ding userid success')
    print("[+]don't forget clear wlan proxy setting")


def get_other_info():
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
            print(req.text)
            recordid = json.loads(req.text)['records'][-1]['recordId']
        return recordid

    def getInfoByRecordId():
        url = 'http://218.75.25.135:81/dingPracticeApply.do?method=editPracticeApply&id={}&view=1'.format(
            get_recoed_id())
        with httpx.Client() as client:
            req = client.get(url, headers=header, cookies=cookie)
            return req.text

    def findInfoFromHtml():
        sel = Selector(getInfoByRecordId())
        global lng
        global lat
        global companyid
        global str5
        global i2
        lng = sel.css('#lng::attr(value)').get()
        lat = sel.css('#lat::attr(value)').get()
        companyid = sel.css('#i1::attr(value)').get()
        str5 = sel.css('#bdate::attr(value)').get()
        i2 = sel.css('#i2::attr(value)').get()

    findInfoFromHtml()
    print('[+]get other info success')
    print('[+]print all info')
    print('[-]ding userid', ding_user_id)
    print('[-]lng', lng)
    print('[-]lat', lat)
    print('[-]companyid', companyid)
    print('[-]str5', str5)
    print('[-]i2', i2)


def write_info_to_file():
    with open('config.json', 'w') as f:
        f.write(
            json.dumps([
                {
                    "ding_id": ding_user_id,
                    "lng": lng,
                    "lat": lat,
                    "companyId": companyid,
                    "random": True,
                    "max_delay": 1800,
                    "str5": str5,
                    "ua": 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19A348 AliApp(DingTalk/6.3.7) com.laiwang.DingTalk/21728861 Channel/201200 language/en-CN UT4Aplus/0.0.6 WK'
                }])
        )
    with open('ding_userid.txt', 'w') as f:
        f.write(ding_user_id)
    with open('info.txt', 'w', encoding='utf-8') as f:
        f.write('ding_id '+ding_user_id+'\n')
        f.write('lng ' + lng+'\n')
        f.write('lat ' + lat+'\n')
        f.write('companyid ' + companyid+'\n')
        f.write('str5 ' + str5+'\n')
        f.write('i2 ' + i2+'\n')


get_ding_id()
get_other_info()
write_info_to_file()
time.sleep(10)
