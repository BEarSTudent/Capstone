import pymysql

def read_db(sql: str):
    db = pymysql.connect(host='127.0.0.1', user='web', password='strweb', db='str_capstone')
    
    cursor = db.cursor()
    
    cursor.execute(sql)
    
    data = cursor.fetchall()
    
    db.close()
    
    return data

def write_db(sql: str):
    db = pymysql.connect(host='127.0.0.1', user='web', password='strweb', db='str_capstone')
    
    cursor = db.cursor()

    cursor.execute(sql)

    db.commit()

    db.close

def user_insert(user_id: str, pw: str, user_name: str):    
    sql = "INSERT INTO str_user(user_id, pw, user_name) VALUES('" + user_id + "', '" + pw + "', '" + user_name + "');"
    write_db(sql)

def user_select(user_id: str):
    sql = "SELECT * FROM str_user WHERE user_id = '" + user_id + "';"

    return read_db(sql)

def user_update(user_id: str, pw: str, user_name: str, user_image: str):
    sql = "UPDATE str_user SET user_id='" + user_id + "', pw='" + pw + "', user_name='" + user_name + "', user_image='" + user_image + "' WHERE user_id='" + user_id + "';"
    
    write_db(sql)
