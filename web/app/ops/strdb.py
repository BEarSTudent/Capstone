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

    return read_db(sql)[0]

def user_update(user_id: str, pw: str, user_name: str, user_image: str):
    sql = "UPDATE str_user SET pw='" + pw + "', user_name='" + user_name + "', user_image='" + user_image + "' WHERE user_id='" + user_id + "';"
    
    write_db(sql)

def board_select_all():
    sql = "SELECT * FROM str_board"
    
    return read_db(sql)

def board_insert(user_id: str, board_date: str, board_image: str, contents: str):
    sql = "INSERT INTO str_board(user_id, board_date, board_image, contents) VALUES('" + user_id + "', '" + board_date + "', '" + board_image + "', '" + contents + "');"
    
    write_db(sql)

def board_update(board_id: int, board_image: str, contents: str):
    sql = "UPDATE str_board SET board_image='" + board_image + "', contents='" + contents + "' WHERE board_id='" + str(board_id) + "';"
    
    write_db(sql)

def board_delete(board_id: int):
    sql = "DELETE FROM str_board WHERE board_id=" + str(board_id) + ";"

    write_db(sql)

def savebox_select(user_id: str):
    sql = "SELECT * FROM str_savebox WHERE user_id='" + user_id + "';"

    return read_db(sql)

def savebox_insert(user_id: str, savebox_image: str):
    sql = "INSERT INTO str_savebox(user_id, savebox_image) VALUES('" + user_id + "', '" + savebox_image + "');"

    write_db(sql)

def savebox_delete(savebox_id: int):
    sql = "DELETE FROM str_savebox WHERE savebox_id=" + str(savebox_id) + ";"

    write_db(sql)

def board_one(board_id: int, user_id: str):
    board_sql = "SELECT * FROM str_board WHERE board_id=" + str(board_id) + ";"
    board_data = read_db(board_sql)[0]

    like_sql = "SELECT COUNT(*) FROM str_like WHERE board_id=" + str(board_id) + ";"
    like_count = int(read_db(like_sql)[0][0])

    comment_sql = "SELECT * FROM str_comment WHERE board_id=" + str(board_id) + ";"
    comment_data = read_db(comment_sql)

    like_user_sql = "SELECT * FROM str_like WHERE board_id=" + str(board_id) + " AND user_id='" + user_id + "';"
    like_user_data = len(read_db(like_user_sql))

    return {'board_data': board_data, 'like_count': like_count, 'comment_data': comment_data, 'like_user_data': like_user_data}

def like_insert(board_id: int, user_id: str):
    sql = "INSERT INTO str_like(board_id, user_id) VALUES(" + str(board_id) + ", '" + user_id + "');"

    write_db(sql)

def like_delete(board_id: int, user_id: str):
    sql = "DELETE FROM str_like WHERE board_id=" + str(board_id) + " AND user_id='" + user_id + "';"

    write_db(sql)

def comment_insert(board_id: int, user_id: str, contents: str):
    sql = "INSERT INTO str_comment(board_id, user_id, contents) VALUES(" + str(board_id) + ", '" + user_id + "', '" + contents + "');"

    write_db(sql)

def comment_delete(comment_id: int):
    sql = "DELETE FROM str_comment WHERE comment_id=" + str(comment_id) + ";"

    write_db(sql)
