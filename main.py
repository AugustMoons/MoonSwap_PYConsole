import time
import function.sql
import function.toml2
import function.api
import function.run_frp
from function.time.times import gettime
import threading
from time import sleep

def frpcommand2(runcommand2):
    function.run_frp.frpcommand(command=runcommand2)

def frpreset(resetcommand2,enable=2):
    function.run_frp.reset(command=resetcommand2, enable=enable)

def main():
    try:
        while True:
            threads = []#存储线程对象
            print(f"{gettime()}  【INFO】SwapMoon断网恢复程序正在启动")
            while True:
                if function.toml2.readconfig()['values'][0]['enabled'] == 'T':
                    print(f"{gettime()}  【INFO】FRP自启动已开启")
                    break
                elif function.toml2.readconfig()['values'][0]['enabled'] == 'F':
                    print(f"{gettime()}  【INFO】FRP自启动已关闭")
                else:
                    print(f"{gettime()}  【INFO】config.toml参数配置错误，请检查后重试")
                    time.sleep(10)
                frpenable1 = input('\n【y】启动FRPC\n【n】重置FRPC初始配置\n输入^c关闭程序(y/n):')
                if frpenable1 == 'y':
                    break
                elif frpenable1 == 'n':
                    data1 = function.toml2.readconfig()
                    data2 = data1['frpcdata'][0]['frp_path']
                    filenames = data1['values'][0]['frptomllist']
                    function.toml2.deltoml(path=data2 + '/proxy/', filenames=filenames)
                    function.sql.resetsql()
                    function.toml2.numup(0)
                    function.toml2.frptomllist_reset()
                    function.toml2.useremoteport_up(remoteport=[])
                    function.toml2.enabled_reset()

            print(f"{gettime()}  【INFO】正在请求映射表数据")
            json_data = function.api.getapidata()
            print(f"{gettime()}  【INFO】正在重置数据库")
            function.sql.resetsql()
            print(f"{gettime()}  【INFO】正在写入数据库")
            for i in json_data['Data']['data']:
                function.sql.writein(i)
            print(f"{gettime()}  【INFO】正在写入配置文件")
            sql_data0 = function.sql.readsql()  # 数据库映射列表数据
            sql_data = []
            for sqldata in sql_data0:
                if sqldata[7] == 'yes':
                    sql_data.append(sqldata)
                else:
                    continue
            function.toml2.write_in_all(sql_data=sql_data)#创建所有子配置文件
            print(f"{gettime()}  【INFO】正在启动FRP")
            config_data = function.toml2.readconfig()
            runcommand2 = config_data['frpcdata'][0]['frp_path']+'/frpc -c '+ config_data['frpcdata'][0]['includes'][0]
            runfrp = threading.Thread(target=frpcommand2,args=(runcommand2,))
            threads.append(runfrp)
            threads[0].start()
            print(f"{gettime()}  【INFO】正在启动控制台")
            print(f"{gettime()}  【INFO】控制台启动成功")
            while True:
                user_input = input("\n请输入代号以启用功能"
                               "\n【1】查询映射数据表"
                               "\n【2】热重载FRP"
                               "\n【3】输入并执行命令"
                               "\n【4】关闭所有FRP项目"
                               "\n【5】启动所有FRP项目"
                               "\n【6】退出FRP并重置程序"
                               "\n【7】修改某项穿透记录状态"
                               "\n Or enter ^C to exit: \n")
                if user_input == '1':#查询映射数据表
                    function.sql.printout()
                    continue
                elif user_input == '2':#热重载FRP
                    print(f"{gettime()}  【INFO】正在热重载")
                    resetcommand1 = function.toml2.readconfig()
                    resetcommand2 = resetcommand1['frpcdata'][0]['frp_path']+'/frpc reload -c '+ resetcommand1['frpcdata'][0]['includes'][0]
                    threads =[]
                    frpreset1 = threading.Thread(target=frpreset,args=(resetcommand2,))
                    threads.append(frpreset1)
                    threads[0].start()
                    continue
                elif user_input == '3':#输入并执行命令
                    command = input('请输入终端命令：')
                    function.run_frp.frpcommand(command=command)
                    continue
                elif user_input == '4' or user_input == '5':
                    if user_input == '4':
                        enable = 0
                        print(f'{gettime()}  【INFO】正在关闭所有FRP项目')
                        function.sql.change_enabled(enable='no')
                        data1 = function.toml2.readconfig()
                        data2 = data1['frpcdata'][0]['frp_path']
                        filenames = data1['values'][0]['frptomllist']
                        function.toml2.deltoml(path=data2 + '/proxy/', filenames=filenames)
                        resetcommand1 = function.toml2.readconfig()
                        resetcommand2 = resetcommand1['frpcdata'][0]['frp_path'] + '/frpc reload -c ' + resetcommand1['frpcdata'][0]['includes'][0]
                        threads = []
                        frpreset1 = threading.Thread(target=frpreset, args=(resetcommand2,enable,))
                        threads.append(frpreset1)
                        threads[0].start()

                    else:
                        enable = 1
                        print(f'{gettime()}  【INFO】正在启动所有FRP项目')
                        function.sql.change_enabled(enable='yes')
                        sql_data = function.sql.readsql()  # 数据库映射列表数据
                        function.toml2.write_in_all(sql_data=sql_data)  # 创建所有子配置文件
                        resetcommand1 = function.toml2.readconfig()
                        resetcommand2 = resetcommand1['frpcdata'][0]['frp_path'] + '/frpc reload -c ' + resetcommand1['frpcdata'][0]['includes'][0]
                        threads = []
                        frpreset1 = threading.Thread(target=frpreset, args=(resetcommand2,enable,))
                        threads.append(frpreset1)
                        threads[0].start()
                    continue

                elif user_input == '6':#退出FRP并重置程序
                    data1 = function.toml2.readconfig()
                    data2 = data1['frpcdata'][0]['frp_path']
                    command = data2+'/frpc stop -c '+data2+'/frpc.toml'
                    filenames = data1['values'][0]['frptomllist']
                    resetfrp = threading.Thread(target=frpcommand2, args=(command,))
                    threads = []
                    threads.append(resetfrp)
                    threads[0].start()
                    sleep(1)
                    function.toml2.deltoml(path=data2+'/proxy/',filenames=filenames)
                    function.sql.resetsql()
                    function.toml2.numup(0)
                    function.toml2.frptomllist_reset()
                    function.toml2.useremoteport_up(remoteport=[])
                    function.toml2.enabled_reset()
                    break
                elif user_input == '7':
                    flag = False
                    user_input2 = input('请输入待修改穿透记录的ID(一次输入限1条)：')
                    sql_data = function.sql.readsql()
                    for i in sql_data:
                        if i[0] == int(user_input2):
                            flag = True
                        else:
                            continue
                    if flag:
                        user_input3 = input(f'【1】关闭穿透记录{user_input2}\n【2】开启穿透记录{user_input2}\n请输入:')
                        print(f'{gettime()}  【INFO】正在修改穿透记录{user_input2}的状态')
                        path = function.toml2.readconfig()['frpcdata'][0]['frp_path']+'/proxy/'
                        filenames = function.toml2.readconfig()['values'][0]['frptomllist']
                        filenames2 = []
                        filename2 = []
                        for filename in filenames:
                            idcode = filename[filename.find('S')+1:filename.find('-')]
                            if idcode == user_input2:
                                filename2.append(filename)
                                continue
                            else:
                                filenames2.append(filename)
                        sql_data = function.sql.readsql()
                        for sqldata in sql_data:
                            if sqldata[0] == int(user_input2):
                                finaldata = sqldata
                        if user_input3 == '1':
                            function.sql.change_one_enabled(enable='no',id=int(user_input2))
                            print(f'{gettime()}  【INFO】正在删除穿透记录{user_input2}的配置文件')
                            function.toml2.deltoml(path=path,filenames=filename2)
                            resetcommand1 = function.toml2.readconfig()
                            resetcommand2 = resetcommand1['frpcdata'][0]['frp_path'] + '/frpc reload -c ' + \
                                            resetcommand1['frpcdata'][0]['includes'][0]
                            threads = []
                            frpreset1 = threading.Thread(target=frpreset, args=(resetcommand2,))
                            threads.append(frpreset1)
                            threads[0].start()
                            config_data = function.toml2.readconfig()
                            config_data['values'][0]['frptomllist'] = filenames2
                            function.toml2.dumptoml(dst_file='./lib/config.toml',data=config_data)

                        else:
                            function.sql.change_one_enabled(enable='yes',id=(user_input2))
                            sql_data = function.sql.readsql()
                            for sqldata in sql_data:
                                if sqldata[0] == int(user_input2):
                                    finaldata = sqldata
                            print(f'{gettime()}  【INFO】正在创建穿透记录{user_input2}的配置文件')
                            function.toml2.open_one(sql_data=finaldata)
                            resetcommand1 = function.toml2.readconfig()
                            resetcommand2 = resetcommand1['frpcdata'][0]['frp_path'] + '/frpc reload -c ' + \
                                            resetcommand1['frpcdata'][0]['includes'][0]
                            threads = []
                            frpreset1 = threading.Thread(target=frpreset, args=(resetcommand2,))
                            threads.append(frpreset1)
                            threads[0].start()


    except Exception as e:
        print(f"{gettime()}  【ERROR】主程序出现异常:{e}")

if __name__ == '__main__':
    main()
