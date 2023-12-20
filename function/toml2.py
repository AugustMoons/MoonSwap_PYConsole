import toml
import os
from datetime import datetime
import random


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

def dumptoml(dst_file,data):#接收映射表数据并写入toml文件
    try:
        with open(dst_file, 'w') as f:
            r = toml.dump(data, f)
            print(f"{gettime()}  【INFO】{dst_file}(创建)写入成功")
    except Exception as e:
        print(f"{gettime()}  【ERROR】(创建)写入{dst_file}时捕获到异常:{e}")
    #dst_file为目标文件路径，目标文件夹下文件不存在时自动创建
    #data为字典类型

def numup(num):#更新num数值
    try:
        dst_file='./lib/config.toml'
        data = toml.load(dst_file)
        data['values'][0]['num'] = num
        dumptoml(dst_file=dst_file,data=data)
    except Exception as e:
        print(f"{gettime()}  【ERROR】更新并写入num到config.toml时捕获到异常:{e}")

def frptomllist_reset():#更新frptomllist数值
    try:
        dst_file='./lib/config.toml'
        data = toml.load(dst_file)
        data['values'][0]['frptomllist'] = []
        dumptoml(dst_file=dst_file,data=data)
    except Exception as e:
        print(f"{gettime()}  【ERROR】重置frptomllist到config.toml时捕获到异常:{e}")

def enabled_reset():#更新enabled数值
    try:
        dst_file='./lib/config.toml'
        data = toml.load(dst_file)
        data['values'][0]['enabled'] = 'F'
        dumptoml(dst_file=dst_file,data=data)
    except Exception as e:
        print(f"{gettime()}  【ERROR】重置enabled到config.toml时捕获到异常:{e}")

def useremoteport_up(remoteport):#更新useremoteport数值
    try:
        dst_file='./lib/config.toml'
        data = toml.load(dst_file)
        if remoteport == []:
            data['values'][0]['useremoteport'] = []
        else:
            data['values'][0]['useremoteport'].append(remoteport)
        dumptoml(dst_file=dst_file,data=data)
    except Exception as e:
        print(f"{gettime()}  【ERROR】更新useremoteport到config.toml时捕获到异常:{e}")

def open_one(sql_data):#创建（删除）穿透记录配置文件
    try:
        print(sql_data)
        data = {'proxies': []}  # 预处理传参字典
        num = readconfig()['values'][0]['num']  # 穿透记录数量
        path1 = readconfig()['frpcdata'][0]['frp_path']+'/proxy/'#子配置文件创建路径
        i = sql_data
        if i[7] == 'yes':
            # 判断并切分协议
            if '+' in i[3]:
                type = i[3].split('+')
            else:
                type = i[3]
            # 判断并取出内网端口区间
            if '-' in i[2]:
                localport = i[2].split('-')
                start = int(localport[0])
                end = int(localport[1])
                localport = []
                for port in range(start,end+1):
                    localport.append(str(port))
            else:
                localport = [i[2]]
            # 以协议数量为循环次数标准
            for h in localport:
                #获取记录中正在使用的外网端口
                useremoteport = readconfig()['values'][0]['useremoteport']
                #生成可用的随机外网端口
                while len(useremoteport) <= 1000:
                    remoteport = random.randint(1000, 2000)
                    if remoteport in useremoteport:
                        continue
                    else:
                        useremoteport_up(remoteport=remoteport)
                        break
                # 每个协议对应多端口分组
                for j in type:
                    num += 1
                    data0 = {'name': '', 'type': '', 'localIP': '', 'localPort': '', 'remotePort': ''}
                    data0['name'] = str(num) + j
                    data0['type'] = j
                    data0['localIP'] = i[1]
                    data0['localPort'] = int(h)
                    data0['remotePort'] = remoteport
                    data['proxies'].append(data0)
                    dumptoml(dst_file=f"{path1}VDS{i[0]}--{i[1]}-{i[2]}.toml", data=data)
            # 传参字典及内网多端口初始化
        data['proxies'] = []
        # 协议列表初始化
        data2 = readconfig()
        data2['values'][0]['frptomllist'].append(f'VDS{i[0]}--{i[1]}-{i[2]}.toml')  # 将创建的子配置文件名记录入config.toml
        dumptoml(dst_file='./lib/config.toml', data=data2)
        print(f"{gettime()}  【INFO】整理数据并配置子配置文件成功")
        numup(num=int(num))

    except Exception as e:
        print(f"{gettime()}  【ERROR】整理数据并配置子配置文件时捕获到异常:{e}")

def write_in_all(sql_data):#整理数据并配置子配置文件
    try:
        data = {'proxies': []}  # 预处理传参字典
        num = readconfig()['values'][0]['num']  # 穿透记录数量
        path1 = readconfig()['frpcdata'][0]['frp_path']+'/proxy/'#子配置文件创建路径
        for i in sql_data:

            if i[7] == 'yes':
                # 判断并切分协议
                if '+' in i[3]:
                    type = i[3].split('+')
                else:
                    type = i[3]
                # 判断并取出内网端口区间
                if '-' in i[2]:
                    localport = i[2].split('-')
                    start = int(localport[0])
                    end = int(localport[1])
                    localport = []
                    for port in range(start,end+1):
                        localport.append(str(port))
                else:
                    localport = [i[2]]
                # 以协议数量为循环次数标准
                for h in localport:
                    #获取记录中正在使用的外网端口
                    useremoteport = readconfig()['values'][0]['useremoteport']
                    #生成可用的随机外网端口
                    while len(useremoteport) <= 1000:
                        remoteport = random.randint(1000, 2000)
                        if remoteport in useremoteport:
                            continue
                        else:
                            useremoteport_up(remoteport=remoteport)
                            break
                    # 每个协议对应多端口分组
                    for j in type:
                        num += 1
                        data0 = {'name': '', 'type': '', 'localIP': '', 'localPort': '', 'remotePort': ''}
                        data0['name'] = str(num) + j
                        data0['type'] = j
                        data0['localIP'] = i[1]
                        data0['localPort'] = int(h)
                        data0['remotePort'] = remoteport
                        data['proxies'].append(data0)
                        dumptoml(dst_file=f"{path1}VDS{i[0]}--{i[1]}-{i[2]}.toml", data=data)
                # 传参字典及内网多端口初始化
            data['proxies'] = []
            # 协议列表初始化
            data2 = readconfig()
            data2['values'][0]['frptomllist'].append(f'VDS{i[0]}--{i[1]}-{i[2]}.toml')  # 将创建的子配置文件名记录入config.toml
            dumptoml(dst_file='./lib/config.toml', data=data2)
        print(f"{gettime()}  【INFO】整理数据并配置子配置文件成功")
        numup(num=int(num))

    except Exception as e:
        print(f"{gettime()}  【ERROR】整理数据并配置子配置文件时捕获到异常:{e}")

def readconfig():#读取toml文件数据
    try:
        data = toml.load('./lib/config.toml')
        return data
    except Exception as e:
        print(f"{gettime()}  【ERROR】读取config.toml时捕获到异常:{e}")

def readfrpc(path):  # 读取toml文件数据
    try:
        data = toml.load(path)
        return data
    except Exception as e:
        print(f"{gettime()}  【ERROR】读取{path}时捕获到异常:{e}")

def deltoml(path,filenames):#删除frp子配置文件
    try:
        for filename in filenames:
            file_path = os.path.join(path,filename)# 构建文件路径
            if os.path.exists(file_path):  # 检查文件是否存在
                os.remove(file_path)  # 删除文件
                print(f"文件 {filename} 已删除")
            else:
                print(f"文件 {filename} 不存在")

    except Exception as e:
        print(f"{gettime()}  【ERROR】删除frp子配置文件时捕获到异常:{e}\n请手动删除")
