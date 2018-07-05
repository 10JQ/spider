import pymysql

# 数据库连接函数      
def connDB():  
    # 打开数据库连接
    db = pymysql.connect("114.215.99.71","root","yan33ppJun9966A","tb_vote")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    return (db, cursor)

# 关闭数据库连接  
def exitConn(db, cursor):
    db.close() 

# 读取数据

# 生成图片

