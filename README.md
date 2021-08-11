# SogangFriend

Pycharm 등 IDE 사용 권장(idle, cmd 불편합니다)
[파이참 학생 무료 Pro버전](https://celebro.tistory.com/1)

## 설치 Step
--------------------
### 0. 이 repository clone
명령어 : __git clone https://github.com/SogangFriend/SogangFriend.git__
또는
1) Github Desktop에서 file -> clone repository -> Github.com 에서 SogangFriend 찾아서 선택 또는 URL에서 위 주소 입력
2) 로컬 패스는 적절히 선택

### 1. virtual environment 별도 설치
명령어 : __python -m venv myvenv__ (myvenv는 가상환경의 이름으로 자유롭게 설정 가능)
        
        <window>
        > pip install virtualenv 
        > virtualenv venv

### 2. virtual environment 실행
명령어 : __source myvenv/bin/activate__ (myvenv -설치한 가상환경 이름- 의 상위 폴더에서 진행해야함)
        
        <window>
        > call venv/scripts/activate
        
### 3. pip 최신으로 업그레이드
명령어 : __python -m pip install --updgrade pip__

### 4. Django 설치
명령어 : __pip install django__

### 5. models가 수정된 커밋을 pull할 경우 migration을 만들어줘야함
명령어 : <br>__python manage.py makemigrations__<br>__python manage.py migrate__

* 주의사항
1. 사람별로 브랜치를 만들 것입니다. <br>본인의 브랜치를 사용하길 권장하며 main 브랜치에 바로 commit-push 하지 않도록 부탁드립니다.<br>

