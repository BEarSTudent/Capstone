# StyleTransfer_Capstone
메인 언어




프론트 엔드

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![JAVASCRIPT](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white)

백엔드

![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![](https://img.shields.io/badge/uWSGI-4EA94B?style=for-the-badge&logo=&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![opencv](https://img.shields.io/badge/opencv-5c3ee8?style=for-the-badge&logo=opencv&logoColor=white)

AI server

![nvida](https://img.shields.io/badge/NVIDIA-RTX2070-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu_20.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![pytorch](https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![mmcv](https://img.shields.io/badge/mmcv-4285F4?style=for-the-badge&logo=mmcv&logoColor=white)
![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Image Generation Server

![nvida](https://img.shields.io/badge/NVIDIA-RTX3080-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![pytorch](https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)


## 프로젝트 개요
STR(Style Transfer for Recollection)팀은 style transfer 기법을 이용하여 웹서비스를 제공하는 프로그램을 제작하는 프로젝트를 진행하였습니다. 

크게 Web과 AI로 나누어 환경을 구성하였습니다. Web에서는 사용자가 이용하는 웹페이지가 구동되는 환경이 구축되어 있고 AI는 Style Transfer, Segmentation 모델 환경이 구축되어 있습니다.

## 기능

### 이미지 변환 기능

<br/>


### 게시판 기능

상단 배너의 [Community]를 통해 **게시판 페이지** 접근 가능

로그아웃 | 로그인
----- | -----
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/0b161f18-afaa-4bde-a2e7-e5f5e237bb5e) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/e45af61a-e7c9-419f-ad25-315774d8124d)

- 게시된 게시물 사진을 보드 형태로 확인 가능
- 로그인 시 우측 하단에 새로운 게시물을 작성할 수 있는 플로팅 버튼 활성화

- 게시물 클릭 시 **팝업창**을 통해 게시글 확인 가능
  
  로그아웃 | 로그인
  ----- | -----
  ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/d78789f5-a40e-4bc1-a1ac-c5702689d470) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/130b0fa3-8a25-4b64-a4bb-2703adfa6ee3)
  
  - 게시물의 사진, 작성자 정보, 제목, 내용, 작성일자, 좋아요, 댓글 확인 가능
  - 로그인 시 좋아요 영역을 클릭하여 좋아요 표시/취소 가능
  - 로그인 시 댓글 작성 영역 활성화

**페이지 하단**

로그아웃 | 로그인
----- | -----
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/6e9fe430-7abd-4835-be17-548c5f6963c3) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/32d4be55-9498-4124-bff0-4663ed12f84c)

(사진은 예시 이미지입니다.)

- 페이지 하단으로 스크롤 시 추가 게시물 로드 (9개 게시물 단위로 로드)
- [Top] 버튼을 통해 페이지 상단으로 이동 가능


**게시물 작성**
- 로그인 시 Community와 Mypage에 활성화되는 우측 하단의 플로팅 버튼을 클릭하면 게시물 작성 팝업창을 통해 새로운 게시물 작성 가능

  ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/ebe2d978-7453-4187-9df2-6ef8938e2998)

  이미지 선택 버튼 클릭 시 | 이미지 선택 시
  ----- | -----
  ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/e692a73c-9d9b-47c9-8f2e-4519bc43ebea) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/1022c720-5bfd-4821-862a-52cedd055128)

  - 업로드 버튼을 통해 새로운 게시물 업로드 가능
  - 게시물 업로드 완료 시 Mypage로 이동
  - 게시물 이미지 선택과 제목 입력 필수

<br/>


### 검색 기능
게시판 페이지의 상단 부분 검색 영역을 통해 검색 가능
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/65cf4ce7-42ab-4281-bc25-e26ee4469ad2)

검색어 기반 검색 | 정렬
----- | -----
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/d322ecf1-7043-4357-b654-7d973673a4b0) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/2f7ffc13-d8e7-4f12-a90f-4ee0af3a05b2)

(예시 이미지입니다.)
- 검색어 입력 시 입력한 검색어가 제목과 본문에 포함된 게시물만 필터링
- 작성일 기반의 '최신순', 좋아요 수 기반의 '인기순', 댓글 수 기반의 '댓글순' 정렬 가능
  - 인기순과 댓글순 정렬의 경우 좋아요 수와 댓글 수가 같은 게시물은 최신순 기반 정렬
- 검색어와 정렬 혼합 검색 가능

<br/>


### 회원 기능

<br/>


### 마이프로필 기능
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/a8d76d2c-1ca3-4e7e-a5af-c81047ee770f)

- 아이디, 이름, 프로필 사진, 게시물 개수, 보관함 개수 확인 가능
- 프로필 편집 시 비밀번호 확인 후 이름과 프로필 사진 변경 가능

  ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/7d70710f-1d04-4a0b-86f4-7ed0b731ab7a) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/b6628768-8744-4523-b2c7-306decc78566)
  ----- | -----

<br/>


### 보관함 기능

게시물 | 보관함
----- | -----
![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/06615e22-e6fd-461e-9a42-c910efc8f2e8) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/4efb5268-1a32-4c94-9d01-d8b5f3b7a24c)

- 로그인 후 mypage 접속 시 사용자가 작성한 게시물과 보관함 확인 가능
- 게시물/보관함 각 텍스트 클릭 시 해당 데이터 출력
- 게시물과 보관함의 사진 클릭 시 해당 게시물/보관함의 정보를 팝업창을 통해 확인 가능

  게시물 | 보관함
  ----- | -----
  ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/98a14fcb-5f29-4fd4-a853-3b94c9d553d3) | ![image](https://github.com/STRCapstone/StyleTransfer_Capstone/assets/94973258/0e64143f-867a-46ab-9a04-d7836e715731)

  - 게시물 팝업은 Community 페이지의 팝업창과 동일
  - 보관함 팝업의 양측 하단 버튼을 통해 다운로드 및 삭제 가능
