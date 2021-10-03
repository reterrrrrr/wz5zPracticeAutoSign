# from ctypes import HRESULT
from asyncio.windows_events import SelectorEventLoop
from math import degrees
import os

a = os.getenv('ENV_')

import argparse

parser = argparse.ArgumentParser(description='')
#type是要传入的参数的数据类型  help是该参数的提示信息
import json


ding_userid = os.getenv('ENV_DING_USERID')
companyId = os.getenv('ENV_COMPANYID')
lng = os.getenv('ENV_LNG')
lat = os.getenv('ENV_LAT')
str5 = os.getenv('ENV_STR5')

print(bool(1-bool(ding_userid)))
parser.add_argument('-c','--conf',type=str,help='conf file path')
if not parser.parse_args().conf:
    parser.add_argument('-d','--ding-userid',type=str,help='dingid',required=not bool(ding_userid))
    parser.add_argument('-C','--companyId',type=str,help='companyId',required=not bool(companyId))
    parser.add_argument('-lng',type=str,help='lng',required=not bool(lng))
    parser.add_argument('-lat',type=str,help='lat',required=not bool(lat))
    parser.add_argument('-s','--str5',type=str,help='str5',required=not bool(str5))
    parser.add_argument('-r','--random',type=bool,help='enable random delay',default=True)
    parser.add_argument('-m','--max-delay-time',type=int,help='enter max delay time',default=1800)

#获得传入的参数
# print(args.a)