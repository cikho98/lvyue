import pymysql


def mysql(database, sql):
    answer = []
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
    desc = cursor.description
    desc = list(desc)
    for j in range(0, len(result)):
        response = {}
        for i in range(0, len(desc)):
            response[desc[i][0]] = result[j][i]
        answer.append(response)
    # 关闭数据库
    cursor.close()
    conn.close()
    return answer


