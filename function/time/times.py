from datetime import datetime


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
        print(f"{year}{day}{minute}")
        return f"{year}{day}{minute}"
    except Exception as e:
        print(f'【ERROR】获取当前时间时捕获到异常：{e}')