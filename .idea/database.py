import pymysql

def databaseOperated(database,sql):
    # 链接数据库
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database=database,
        charset='utf8'
    )
    # 链接数据库
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    # 关闭数据库
    cursor.close()
    conn.close()
    return result