import requests
from datetime import datetime
import toml

def gettime():#获取当前时间,时间格式返回
    now = datetime.now()
    years = str(now.year)
    month = now.month
    month = "{:02d}".format(month)
    day = now.day
    day = "{:02d}".format(day)
    hours = now.hour
    hours = "{:02d}".format(hours)
    minute = now.minute
    minute = "{:02d}".format(minute)
    second = now.second
    second = "{:02d}".format(second)
    time = years+'/'+month+'/'+day+' '+hours+':'+minute+':'+second
    return time

def get_time():#获取当前时间,api格式返回
    try:
        now = datetime.now()
        year = str(now.year)[2:]
        day = now.day
        day = "{:02d}".format(day)
        minute = now.minute
        minute = "{:02d}".format(minute)
        return f"{year}{day}{minute}"
    except Exception as e:
        print(f'【ERROR】获取当前时间时捕获到异常：{e}')

def getapidata():#通过api获取映射表数据
    try:
        #发起GET请求
        response = requests.get(getapi())
        if response.status_code == 200:
            #请求成功返回数据
            data = response.json()
            print(f'{gettime()}  【INFO】请求成功')
            return data
        else:
            #请求失败返回错误代码
            error = response.status_code
            return error
    except Exception as e:
        print(f'{gettime()}  【ERROR】api调用时捕获到异常：{e}')


def getapi():#计算api接口链接
    try:
        time = get_time()
        SID1 = toml.load('./lib/api.toml')['SID1']
        SID2 = toml.load('./lib/api.toml')['SID2']
        if SID2*SID1 == 1:
            print(f'{gettime()}  【WARNING】SID数值安全性过低,为了安全请重新设置SID值')
        ip = toml.load('./lib/api.toml')['ip']
        key = 'key='+toml.load('./lib/api.toml')['key']
        id = 'id='+toml.load('./lib/api.toml')['id']
        username = 'username='+toml.load('./lib/api.toml')['username']
        passwd = 'passwd='+toml.load('./lib/api.toml')['passwd']
        sid = str(int(time)*SID1+SID2)
        URL = ip+key+'&'+id+'&'+username+'&'+passwd+'&sid='+sid
        return URL
    except Exception as e:
        print(f'{gettime()}  【ERROR】计算api接口URL时捕获到异常：{e}')

