# Install & Drive Guide
## 목차

1. [Install Guide](#Install-Guide)

    1. [docker Ubuntu 이미지 설치](#1-Ubuntu-22.04-설치)
    2. [가상환경 설치](#2-가상환경-설치)
    3. [라이브러리 설치](#3-라이브러리-설치)
2. [Drive Guide](#Drive-Guide)
    1. [패키지 설치](#1-패키지-설치)
    2. [mysql 설정](#2-mysql-설정)
    3. [uwsgi.ini & uwsgi.log 생성](#3-uwsgiini--uwsgilog-생성)
    4. [nginx 설정](#4-nginx-설정)
    5. [bashrc 설정](#5-bashrc-설정)
    6. [실행](#6-실행)
## Install Guide
### 1. Ubuntu 22.04 설치
docker에서 ubuntu 22.04 이미지를 다운받아줍니다.

### 2. 가상환경 설치
차례대로 터미널에 입력해주세요

```
sudo apt update
sudo apt install curl -y
curl --output anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
sha256sum anaconda.sh
bash anaconda.sh
sudo vi ~/.bashrc
export PATH=~/anaconda3/bin:~/anaconda3/condabin:$PATH
source ~/.bashrc
conda create -n capstone python=3.8
conda activate capstone
```
### 3. 라이브러리 설치
```
conda install -y pillow flask flask-login requests pymysql uwsgi
```

## Drive Guide
### 1. 패키지 설치
```
sudo apt install -y mysql-server nginx
```
### 2. mysql 설정
데이터베이스 생성
```
CREATE DATABASE str_capstone;
USE str_capstone;
```
테이블 생성
```
CREATE TABLE str_user (
user_id VARCHAR(30) PRIMARY KEY,
pw VARCHAR(128) NOT NULL,
user_name VARCHAR(30) NOT NULL,
user_image VARCHAR(250)
);
```
```
CREATE TABLE str_board (
board_id INT AUTO_INCREMENT PRIMARY KEY,
user_id VARCHAR(30) NOT NULL, FOREIGN KEY(user_id) REFERENCES str_user(user_id) ON DELETE CASCADE,
board_date DATETIME NOT NULL,
board_image VARCHAR(250) NOT NULL,
board_title TEXT,
contents TEXT
);
```
```
CREATE TABLE str_savebox (
savebox_id INT AUTO_INCREMENT PRIMARY KEY,
user_id VARCHAR(30) NOT NULL, FOREIGN KEY(user_id) REFERENCES str_user(user_id) ON DELETE CASCADE,
savebox_image VARCHAR(250) NOT NULL
);
```
```
CREATE TABLE str_like (
board_id INT, FOREIGN KEY(board_id) REFERENCES str_board(board_id) ON DELETE CASCADE,
user_id VARCHAR(30), FOREIGN KEY(user_id) REFERENCES str_user(user_id) ON DELETE CASCADE,
PRIMARY KEY (board_id, user_id)
);
```
```
CREATE TABLE str_comment (
comment_id INT AUTO_INCREMENT PRIMARY KEY,
board_id INT NOT NULL, FOREIGN KEY(board_id) REFERENCES str_board(board_id) ON DELETE CASCADE,
user_id VARCHAR(30) NOT NULL, FOREIGN KEY(user_id) REFERENCES str_user(user_id) ON DELETE CASCADE,
contents TEXT
);
```
web 코드에서 사용할 사용자 생성
```
CREATE USER 'web'@'localhost' IDENTIFIED BY '[password]';
GRANT SELECT, INSERT, UPDATE, DELETE ON str_capstone.str_user TO 'web'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON str_capstone.str_board TO 'web'@'localhost';
GRANT SELECT, INSERT, DELETE ON str_capstone.str_savebox TO 'web'@'localhost';
GRANT SELECT, INSERT, DELETE ON str_capstone.str_like TO 'web'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON str_capstone.str_comment TO 'web'@'localhost';
```
keys.xml 생성
```
cd StyleTransfer_Capstone/web/app
```
```
<?xml version="1.0" encoding="utf-8"?>

<resources>
    ...
    <string name="db_web_pw">[password]</string>
    ...
</resources>

```
### 3. uwsgi.ini & uwsgi.log 생성
```
cd StyleTransfer_Capstone/web/app
vi uwsgi.log # 생성만하면 됩니다.
vi uwsgi.ini
```
아래 내용을 입력해주세요.
```
[uwsgi]
module = __init__
callable = app

socket = /tmp/capstone.sock
chmod-socket = 666
vacuum = true
processes = 4
threads = 8

daemonize = /home/capstone/strproject/web/app/uwsgi.log

die-on-term = true

# 가상 환경 설정
home = /home/capstone/anaconda3/envs/capstone

# 환경 변수 설정
env = PYTHONPATH=/home/capstone/anaconda3/envs/capstone/lib/python3.8

chdir = /home/capstone/strproject/web/app
```
### 4. nginx 설정
```
sudo vim /etc/nginx/sites-enabled/default
```
```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;
    server_name capstone.juyeolweb.site juyeolweb.site;

    location / {
        try_files $uri @app;
        client_max_body_size 20M;
    }

    location @app {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/capstone.sock;
    }
}
```

### 5. bashrc 설정
```
service ssh restart
service mysql restart
su - capstone -c "/home/capstone/anaconda3/envs/capstone/bin/uwsgi --ini /home/capstone/strproject/web/app/uwsgi.ini"
service nginx restart
```


### 6. 실행
```
cd StyleTransfer_Capstone/web/app
uwsgi --ini uwsgi.ini
sudo nginx restart
```