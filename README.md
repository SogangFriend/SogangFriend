# SogangFriend
교내의 고향 친구 및 이웃 친구를 찾는 웹사이트 개발 프로젝트!


--------------------
## Database Relations
![](https://user-images.githubusercontent.com/63971146/138544000-e98ce60d-86c2-4761-bc24-89b7d2432d43.png)

## Components
- 이메일 인증을 통한 회원가입
- 위치 인증을 이용한 같은 동네 사용자 찾기
- 같은 동네 사용자 간 취미 공유
- 단체 채팅방, DM 기능

## Design Prototype
### Homepage
<img src="https://user-images.githubusercontent.com/63971146/138401542-32426e82-e3cd-4a23-8a8e-2ca92723566f.png" width=70%/>

### Signup page
<img src="https://user-images.githubusercontent.com/63971146/138401722-38b0ea7c-f67c-470f-ae82-eb1e95657827.png" width=70%/>
<img src="https://user-images.githubusercontent.com/63971146/138401808-0a5d7a2a-1d12-40dd-95a6-613624a902a0.png" width=70%/>

### Chat page
<img src="https://user-images.githubusercontent.com/63971146/138402138-0cf1185b-470f-4fc2-b98d-5d416757396a.png" width=70%/>

## Used tools & Reference documents
- [Django mails](https://docs.djangoproject.com/en/3.2/topics/email/) for Email Authentication
- [Django Channels](https://channels.readthedocs.io/en/stable/) for Chat Service
- [Kakao map API](https://apis.map.kakao.com/web/) for Map, Reverse Geocoding


----------------------------------------------------------------------

## 설치 Guide
Pycharm 등 IDE 사용 권장(idle, cmd 불편합니다)
[파이참 학생 무료 Pro버전](https://celebro.tistory.com/1)

### 0. 이 repository clone
명령어 : __git clone https://github.com/SogangFriend/SogangFriend.git__
또는
1) Github Desktop에서 file -> clone repository -> Github.com 에서 SogangFriend 찾아서 선택 또는 URL에서 위 주소 입력
2) 로컬 패스는 적절히 선택

### 1. virtual environment 별도 설치
명령어 : __python -m venv myvenv__ (myvenv는 가상환경의 이름으로 자유롭게 설정 가능)
    

### 2. virtual environment 실행
명령어 : __source myvenv/bin/activate__ (myvenv -설치한 가상환경 이름- 의 상위 폴더에서 진행해야함)
        
        <window>
        > myvenv\Scripts\activate
        
### 3. pip 최신으로 업그레이드
명령어 : __python -m pip install --updgrade pip__

### 4. Django 설치
명령어 : __pip install django__

        pip install -r .\requirements.txt

### 5. models가 수정된 커밋을 pull할 경우 migration을 만들어줘야함
명령어 : <br>__python manage.py makemigrations__<br>__python manage.py migrate__

        <window>
        ※관리자권한으로 파워쉘 실행
        > ExecutionPolicy      <-- 현재 상태 확인
        Restricted        <---- 모든 스크립트 막음

        > Set-ExecutionPolicy Unrestricted  <---풀어줌

        > ExecutionPolicy       <-- 다시 확인
        Unrestricted     <---- 모든 스크립트 허용으로 변경 확인

        >python manage.py makemigrations
        >python manage.py migrate
        
* 주의사항
1. 사람별로 브랜치를 만들 것입니다. <br>본인의 브랜치를 사용하길 권장하며 main 브랜치에 바로 commit-push 하지 않도록 부탁드립니다.
