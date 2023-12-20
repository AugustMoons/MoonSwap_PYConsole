import sqlite3
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

def resetsql():#重置数据表
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        cretask = '''CREATE TABLE IF NOT EXISTS mapping(
            id INT, 
            lan_addr TEXT, 
            lan_port TEXT, 
            protocol TEXT,  
            interface TEXT,
            wan_port TEXT,
            comment TEXT, 
            enabled TEXT 
            )'''#ID编号，内网IP，内网端口，协议，外网地址，外部端口，备注，状态

        drop = "drop table if exists mapping"
        cur.execute(drop)
        db.commit()
        cur.execute(cretask)
        db.commit()
        cur.close()
        db.close()
        print(f'{gettime()}  【INFO】数据库重置成功')
    except Exception as e:
        print(f"{gettime()}  【ERROR】重置数据表时捕获到异常:{e}")


def writein(json_data):#写入数据表
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        cur.execute("INSERT INTO mapping VALUES(?,?,?,?,?,?,?,?)",(json_data['id'],json_data['lan_addr'],json_data['lan_port'],json_data['protocol'],json_data['interface'],json_data['wan_port'],json_data['comment'],json_data['enabled']))
        db.commit()
        cur.close()
        db.close()
        print(f"{gettime()}  【INFO】数据表项目id:{json_data['id']}写入成功")
    except Exception as e:
        print(f"{gettime()}  【ERROR】写入数据到数据表时捕获到异常:{e}")

def printout():#打印数据库列表
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM mapping")
        db.commit()
        data = cur.fetchall()
        data.insert(0,("id","lan_addr","lan_port","protocol","interface","wan_port","comment","enabled"))
        print(f"{gettime()}  【INFO】打印数据如下:\n")
        for i in data:
            print(i)
        cur.close()
        db.close()
    except Exception as e:
        print(f"{gettime()}  【ERROR】打印数据表内容时捕获到异常:{e}")

def readsql():#返回数据库列表
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM mapping")
        db.commit()
        data = cur.fetchall()
        cur.close()
        db.close()
        return data
    except Exception as e:
        print(f"{gettime()}  【ERROR】返回数据表内容时捕获到异常:{e}")

def change_enabled(enable):#修改任务状态:
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        up = f"UPDATE mapping SET enabled = ?"
        cur.execute(up,(enable,))
        db.commit()
        cur.close()
        db.close()
        print(f"{gettime()}  【INFO】数据库任务状态修改成功，enabled更改为:{enable}")
    except Exception as e:
        print(f"{gettime()}  【ERROR】修改数据库任务时捕获到异常:{e}")

def change_one_enabled(enable,id):
    try:
        db = sqlite3.connect('./lib/data.db')
        cur = db.cursor()
        up = f"UPDATE mapping SET enabled = ? where id == ?"
        cur.execute(up,(enable,id,))
        db.commit()
        cur.close()
        db.close()
        print(f"{gettime()}  【INFO】数据库任务状态修改成功，穿透任务{id}的enabled更改为:{enable}")
    except Exception as e:
        print(f"{gettime()}  【ERROR】修改数据库任务时捕获到异常:{e}")


