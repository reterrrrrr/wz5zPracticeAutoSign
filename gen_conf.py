import json
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-d','--dingUserid',nargs='*',type=str,help='dingid',required=True)
parser.add_argument('-c','--companyId',nargs='*',type=str,help='companyId',required=True)
parser.add_argument('-lng',type=str,nargs='*',help='lng',required=True)
parser.add_argument('-lat',type=str,nargs='*',help='lat',required=True)
parser.add_argument('-s','--str5',nargs='*',type=str,help='str5',required=True)
parser.add_argument('-r','--random',nargs='*',type=bool,help='enable random delay',default=True)
parser.add_argument('-m','--max-delay-time',nargs='*',type=int,help='enter max delay time sec',default=900)
parser.add_argument('-ua','--UserAgent',nargs='*',type=str,help='enable User Agent',default='Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18H17 AliApp(DingTalk/6.0.31) com.laiwang.DingTalk/15216879 Channel/201200 language/zh-Hans-CN UT4Aplus/0.0.6 WK')
parser.add_argument('-o','--out-path',type=str,help='enter out path',required=False)
args = parser.parse_args()
data = []
for i in range(len(args.dingUserid)):
    data += [{'ding_id':args.dingUserid[i],'lng':args.lng[i],'lat':args.lat[i],'companyId':args.companyId[i],'random':args.random,'max_delay':args.max_delay_time,'str5':args.str5[i],'ua':args.UserAgent}]
print(json.dumps(data))