import pymysql
import xml.etree.ElementTree as elemTree

def connect_str_db():
    tree = elemTree.parse("web/keys.xml")
    db_pw = tree.find('string[@name="db_web_pw"]').text
    return pymysql.connect(host='127.0.0.1', user='web', password=db_pw, db='str_capstone')

def read_db(db, sql: str):
    """데이터베이스에서 데이터를 읽어올 때 사용하는 함수

    Args:
        db: 연결된 데이터베이스
        sql (str): str형식으로 입력받는 sql 구문

    Returns:
        tuple: 데이터베이스에서 읽어온 tuple 형식의 데이터
    """
    cursor = db.cursor()
    
    cursor.execute(sql)
    
    return cursor.fetchall()

def write_db(db, sql: str):
    """데이터베이스에 데이터를 조작하고 업데이트하는 함수

    Args:
        db: 연결된 데이터베이스
        sql (str): str 형식의 sql 구문
    """
    cursor = db.cursor()

    cursor.execute(sql)

    db.commit()

def user_insert(user_id: str, pw: str, user_name: str):
    """str_user table에 user data를 insert하는 함수

    Args:
        user_id (str): 사용자 id
        pw (str): 해시함수로 암호화된 비밀번호
        user_name (str): 사용자 이름(닉네임)
    """
    db = connect_str_db()
    sql = "INSERT INTO str_user(user_id, pw, user_name) VALUES('" + user_id + "', '" + pw + "', '" + user_name + "');"
    
    write_db(db, sql)
    
    db.close()

def user_select(user_id: str):
    """str_user table에서 사용자를 찾아 데이터를 반환하는 함수

    Args:
        user_id (str): 검색할 user의 id

    Returns:
        tuple: 검색된 user의 tuple 형식의 데이터. (user_id, pw, user_name, user_image)
    """
    db = connect_str_db()
    sql = "SELECT * FROM str_user WHERE user_id = '" + user_id + "';"

    data = read_db(db, sql)[0]
    
    db.close()

    return data

def user_update(user_id: str, pw: str, user_name: str, user_image: str):
    """str_user table의 데이터를 업데이트하는 함수

    Args:
        user_id (str): 업데이트할 사용자의 id
        pw (str): 해시함수로 암호화된 비밀번호
        user_name (str): 사용자 이름(닉네임)
        user_image (str): 사용자의 프로필 사진 경로
    """
    db = connect_str_db()
    sql = "UPDATE str_user SET pw='" + pw + "', user_name='" + user_name + "', user_image='" + user_image + "' WHERE user_id='" + user_id + "';"

    write_db(db, sql)
    
    db.close()

def board_select_all():
    """str_board table의 모든 게시물 데이터를 반환하는 함수

    Returns:
        tuple: 모든 게시물 데이터. ((board_id, user_id, board_date, board_image, contents), ...)
    """
    db = connect_str_db()
    sql = "SELECT * FROM str_board"
    
    data = read_db(db, sql)
    
    db.close()
    
    return data

def board_insert(user_id: str, board_date: str, board_image: str, contents: str):
    """str_board table에 게시물 데이터를 추가하는 함수

    Args:
        user_id (str): 작성자 id
        board_date (str): 작성일자. "YY-MM-DD HH:MM:SS"
        board_image (str): 사진 경로
        contents (str): 게시물 본문 내용
    """
    db = connect_str_db()
    sql = "INSERT INTO str_board(user_id, board_date, board_image, contents) VALUES('" + user_id + "', '" + board_date + "', '" + board_image + "', '" + contents + "');"
    
    write_db(db, sql)
    
    db.close()

def board_update(board_id: int, board_image: str, contents: str):
    """str_board table의 데이터를 업데이트하는 함수

    Args:
        board_id (int): 업데이트할 게시물의 id
        board_image (str): 사진 경로
        contents (str): 게시물 본문 내용
    """
    db = connect_str_db()
    sql = "UPDATE str_board SET board_image='" + board_image + "', contents='" + contents + "' WHERE board_id='" + str(board_id) + "';"
    
    write_db(db, sql)
    
    db.close()

def board_delete(board_id: int):
    """str_board table의 게시물 데이터를 삭제하는 함수

    Args:
        board_id (int): 삭제할 게시물의 id
    """
    db = connect_str_db()
    sql = "DELETE FROM str_board WHERE board_id=" + str(board_id) + ";"

    write_db(db, sql)
    
    db.close()

def savebox_select(user_id: str):
    """str_savebox table에서 사용자의 보관함 데이터를 반환하는 함수

    Args:
        user_id (str): 사용자의 id

    Returns:
        tuple: 사용자의 보관함 데이터. ((savebox_id, user_id, savebox_image), ...)
    """
    db = connect_str_db()
    sql = "SELECT * FROM str_savebox WHERE user_id='" + user_id + "';"

    data = read_db(db, sql)
    
    db.close()
    
    return data

def savebox_insert(user_id: str, savebox_image: str):
    """str_savebox table에 사용자의 사진을 추가하는 함수

    Args:
        user_id (str): 사용자 id
        savebox_image (str): 추가할 사진 경로
    """
    db = connect_str_db()
    sql = "INSERT INTO str_savebox(user_id, savebox_image) VALUES('" + user_id + "', '" + savebox_image + "');"

    write_db(db, sql)
    
    db.close()

def savebox_delete(savebox_id: int):
    """str_savebox table에서 사용자의 사진을 삭제하는 함수

    Args:
        savebox_id (int): 삭제할 보관함 데이터의 id
    """
    db = connect_str_db()
    sql = "DELETE FROM str_savebox WHERE savebox_id=" + str(savebox_id) + ";"

    write_db(db, sql)
    
    db.close()

def board_one(board_id: int, user_id: str):
    """str_board의 한 게시물 데이터에 관련된 데이터들를 반환하는 함수

    Args:
        board_id (int): 게시물 id
        user_id (str): 해당 내용을 조회하는 사용자 id

    Returns:
        dictionary: 게시물에 관련된 데이터 dictionary. {'board_data': board_data, 'user_data': user_data, 'like_count': like_count, 'comment_data': comment_data, 'like_user_data': like_user_data}
    """
    db = connect_str_db()
    
    board_sql = "SELECT * FROM str_board WHERE board_id=" + str(board_id) + ";"
    board_data = read_db(db, board_sql)[0]
    
    user_sql = "SELECT * FROM str_user WHERE user_id = '" + board_data[1] + "';"
    user_data = read_db(db, sql)[0]

    like_sql = "SELECT COUNT(*) FROM str_like WHERE board_id=" + str(board_id) + ";"
    like_count = int(read_db(db, like_sql)[0][0])

    comment_sql = "SELECT * FROM str_comment WHERE board_id=" + str(board_id) + ";"
    comment_data = read_db(db, comment_sql)

    like_user_sql = "SELECT * FROM str_like WHERE board_id=" + str(board_id) + " AND user_id='" + user_id + "';"
    like_user_data = len(read_db(db, like_user_sql))

    db.close()

    return {'board_data': board_data, 'user_data': user_data, 'like_count': like_count, 'comment_data': comment_data, 'like_user_data': like_user_data}

def like_insert(board_id: int, user_id: str):
    """str_like table에 데이터를 추가하여 좋아요를 추가하는 함수

    Args:
        board_id (int): 게시물 id
        user_id (str): 좋아요를 누르는 사용자 id
    """
    db = connect_str_db()
    sql = "INSERT INTO str_like(board_id, user_id) VALUES(" + str(board_id) + ", '" + user_id + "');"

    write_db(db, sql)
    
    db.close()

def like_delete(board_id: int, user_id: str):
    """str_like table에서 데이터를 삭제하여 좋아요를 취소하는 함수

    Args:
        board_id (int): 게시물 id
        user_id (str): 좋아요를 취소하는 사용자 id
    """
    db = connect_str_db()
    sql = "DELETE FROM str_like WHERE board_id=" + str(board_id) + " AND user_id='" + user_id + "';"

    write_db(db, sql)
    
    db.close()

def comment_insert(board_id: int, user_id: str, contents: str):
    """str_comment에 댓글 데이터를 추가하는 함수

    Args:
        board_id (int): 게시물 id
        user_id (str): 댓글을 작성하는 사용자 id
        contents (str): 댓글 내용
    """
    db = connect_str_db()
    sql = "INSERT INTO str_comment(board_id, user_id, contents) VALUES(" + str(board_id) + ", '" + user_id + "', '" + contents + "');"

    write_db(db, sql)
    
    db.close()

def comment_delete(comment_id: int):
    """str_comment table에서 댓글 데이터를 삭제하는 함수

    Args:
        comment_id (int): 댓글 id
    """
    db = connect_str_db()
    sql = "DELETE FROM str_comment WHERE comment_id=" + str(comment_id) + ";"
    
    write_db(db, sql)
    
    db.close()
