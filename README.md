# SogangFriend

## 설치 Step
--------------------

### 1. virtual environment 별도 설치
명령어 : __python -m venv myvenv__ (myvenv는 가상환경의 이름으로 자유롭게 설정 가능)

### 2. virtual environment 실행
명령어 : __source myvenv/bin/activate__ (myvenv -설치한 가상환경 이름- 의 상위 폴더에서 진행해야함)

### 3. pip 최신으로 업그레이드
명령어 : __python -m pip install --updgrade pip__

### 4. Django 설치
명령어 : __pip install django__

### 5. 장고 프로젝트 시작 
명령어 : __django-admin startproject SGFriend .
. 을 꼭 찍어야 하며, SGFriend는 임의의 이름입니다.

### 6. 위의 설치가 완료되면 main 브랜치의 코드를 다운받아 기존을 대체

### 7. models가 수정된 커밋을 pull할 경우 migration을 만들어줘야함
명령어 : <br>__python manage.py makemigrations__<br>__python manage.py migrate__

* 주의사항
1. 사람별로 브랜치를 만들 것입니다. <br>본인의 브랜치를 사용하길 권장하며 main 브랜치에 바로 commit-push 하지 않도록 부탁드립니다.<br>

