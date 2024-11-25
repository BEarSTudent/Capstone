# Install & Drive Guide
## 목차
1. [환경](#환경)
2. [Install Guide](#Install-Guide)
    1. [docker Ubuntu 이미지 설치](#1-Ubuntu-22.04-설치)
    2. [가상환경 설치](#2-가상환경-설치)
    3. [라이브러리 설치](#3-라이브러리-설치)
3. [Drive Guide](#Drive-Guide)
    1. [패키지 설치](#1-패키지-설치)
    2. [mysql 설정](#2-mysql-설정)
    3. [ViT-Adapter git clone](#3-vit-adapter-git-clone)
    4. [ops 파일 생성 및 실행](#4-ops-파일-생성-및-실행)
    5. [pretrain weight 다운](#5-pretrain-weight-다운)
    6. [flask 실행](#6-flask-실행)
4. [Diffusion Model GPU 사용 방법](#diffusion-model-gpu-사용-방법)
## 환경
#### Ubuntu 22.04, CUDA >= 12.1, VRAM >= 12~13GiB

## Install Guide
### 1. Ubuntu 22.04 설치
ubuntu 22.04 를 설치해줍니다.

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
```
### 3. 라이브러리 설치

conda_requirements.txt에 필요한 라이브러리가 적혀있습니다. 실행하면 자동으로 설치됩니다.
```
conda env create -f conda_requirements.txt
```

## Drive Guide
### 1. 패키지 설치
```
sudo apt install -y mariadb-server mariadb-client
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

### 3. ViT-Adapter git clone
```
cd src
git clone https://github.com/czczup/ViT-Adapter.git
```

### 4. ops 파일 생성 및 실행
```
cd ViT-Adapter/segmentation
ln -s ../detection/ops ./
cd ops & sh make.sh
```
만약 sh make.sh가 작동하지 않는다면 아래를 실행해 주세요.
```
./make.sh
```

### 5. pretrain weight 다운
![스크린샷 2024-05-21 오후 9 29 57](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/56315335/c1bf0b3a-9da6-46d7-8c77-b597b9e9a1c9)

다운로드 받은 파일을 src/release 안에 넣어주세요

### 6. flask 실행
최상위 폴더로 이동하신 후 아래 코드를 터미널에 입력해주세요
```
flask run --host 0.0.0.0 --post 2190
```

## Diffusion Model GPU 사용 방법
app.py안의 Generation 객체를 생성하는 코드에 아래와 같이 변경해주시면 생성모델이 GPU에서 동작하게 됩니다.(default: cpu)
```
gen_model = Generation() -> gen_model = Generation(cuda=True)
```