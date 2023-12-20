import subprocess
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


def frpcommand(command):#在终端执行命令
    try:
        # 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # 检查命令是否成功执行
        if result.returncode == 0:
            # 打印命令输出
            print(f"{gettime()}  【INFO】Command output:{result.stdout}")
        else:
            # 打印错误消息
            print(f"{gettime()}  【ERROR】执行命令时出现错误，报错信息为：\n{result.stderr}")
    except Exception as e:
        print(f"{gettime()}  【ERROR】执行runcommand函数(在终端执行命令)时捕获到异常:{e}")


def reset(command,enable):#热重载
    try:
        # 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            # 打印命令输出
            if enable == 1:
                print(f'{gettime()}  【INFO】启动所有FRP项目成功')
            elif enable == 0:
                print(f'{gettime()}  【INFO】关闭所有FRP项目成功')
            print(f"{gettime()}  【INFO】Command output:\n{result.stdout}")
            print(f'{gettime()}  【INFO】热重载成功')
        else:
            # 打印错误消息
            print(f"{gettime()}  【ERROR】执行命令时出现错误，报错信息为：\n{result.stderr}")
    except Exception as e:
        print(f"{gettime()}  【ERROR】执行reset函数(热重载)时捕获到异常:{e}")