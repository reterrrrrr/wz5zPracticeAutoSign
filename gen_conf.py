import json
import os
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-d','--ding-userid',type=str,help='dingid',required=True)
parser.add_argument('-C','--companyId',type=str,help='companyId',required=True)
parser.add_argument('-lng',type=str,help='lng',required=True)
parser.add_argument('-lat',type=str,help='lat',required=True)
parser.add_argument('-s','--str5',type=str,help='str5',required=True)
parser.add_argument('-r','--random',type=bool,help='enable random delay',default=True)
parser.add_argument('-m','--max-delay-time',type=int,help='enter max delay time sec',default=1800)

ding_userid = os.getenv('ENV_DING_USERID')
companyId = os.getenv('ENV_COMPANYID')
lng = os.getenv('ENV_LNG')
lat = os.getenv('ENV_LAT')
str5 = os.getenv('ENV_STR5')