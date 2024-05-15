import pymysql

def user_insert(user_id: str, pw: str, user_name: str):
    db = pymysql.connect(host='127.0.0.1', user='web', password='strweb', db='str_capstone')
    
    cursor = db.cursor()
    
    sql = "INSERT INTO str_user(user_id, pw, user_name) VALUES('" + user_id + "', '" + pw + "', '" + user_name + "');"
    cursor.execute(sql)

    db.commit()
    db.close()

def user_select(user_id: str):
    db = pymysql.connect(host='127.0.0.1', user='web', password='strweb', db='str_capstone')
    
    cursor = db.cursor()
    
    sql = "SELECT * FROM str_user WHERE user_id = '" + user_id + "';"
    cursor.execute(sql)

    data = cursor.fetchone()
    
    db.close()

    return data

def user_update(user_id: str, pw: str, user_name: str, user_image: str):
    db = pymysql.connect(host='127.0.0.1', user='web', password='strweb', db='str_capstone')
    
    cursor = db.cursor()
    
    sql = "UPDATE str_user SET user_id='" + user_id + "', pw='" + pw + "', user_name='" + user_name + "', user_image='" + user_image + "' WHERE user_id='" + user_id + "';"
    print(sql)
    cursor.execute(sql)

    db.commit()
    db.close()
