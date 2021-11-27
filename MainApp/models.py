from django.db import models


# ex) Location : 서울특별시 마포구 대흥동
#               Do - null
#               Si - Seoul
#                   do = null
#                   isGYorTB = true
#               Gu - Mapo
#               Dong - Daeheung


class Location(models.Model):
    do = models.CharField(max_length=20, null=True, blank=True)
    si = models.CharField(max_length=20, null=False)
    isGYorTB = models.BooleanField(default=False)
    gu = models.CharField(max_length=20, null=True, blank=True)
    dong = models.CharField(max_length=20, null=False)

# 데이터베이스 테이블
# class - 테이블 하나에 매칭
# 테이블 도, 시, 구, 동, location, Member
# 도 시 구 동 도 위에 있는 것처럼 외래키를 적절히 써서 서로 참조
# 도 <- 시 <- 구 <- 동
#      시 <- 동
# location 도 시 구 동을 모아주는 역할 (외래키 - 다른 테이블을 참조)
# Member location 외래키 (location을 참조)

# 도 안에 시가 있는 거죠
# 충청남도 안에 천안시 공주시 등등이 있다
# 충청남도라는 데이터가 사라져요
# 천안시 공주시도 같이 사라져요
# 충청남도 없이 천안시 공주시가 있을 순 없으니
# OneToMany, OneToOne, ManyToMany
# Location - Member : OneToMany -> 지역은 하나만, 변경할 수는 있게

# MVC 패턴 아세용? 들어보셨어용?
# Model - View - Controller 의 약자인데
# Model - 데이터베이스에서 관리하는 테이블 (Member, Location 등)
# View - template처럼 Html이나 JS 로 만든 url로 접속하면 보여줘야할 화면
# Controller - View에 대응하는 로직을 담당 예를 들어 SGfriend.com 접속 -> return home.html
# 회원가입 버튼을 눌러요 : SGfriend.com/signup 으로 접속 -> 회원가입 폼을 생성해서 View에 넘겨줘요 View에서 폼을 해석해서 화면에 뿌려요
# 회원가입 완료를 눌러요 : 사용자한테 보이는 url은 아니지만 SGfirend.com/signup/done -> 대응되는 함수나 클래스
# -> 폼에 입력받은 정보가 다 valid한지, 인증도 다 완료됐는지 검사를 하는 로직

# MVC 패턴 Model View Controller 모두 따로 작업한다 하지만 서로 의존적이다

# 장고에서 헷갈릴 수 있는데, Model -> models.py, View -> template, Controller -> views.py

# 채팅에 대한 모델(테이블) 채팅에 어떤 column (field)가 들어갈지
# 뷰를 짜야겠죠
# model -> 채팅만 하면 거의 완성
# view -> 멋들어지게 만들지말고 최대한 간단하게 css 없어도 돼요 어떤 버튼인지 동작만 하게 우선 만들기
# ** controller -> 로직을 잘 수행해야겠죠 **

# 로그인 하고 나서 <-> 하기 전이랑 다르게 (학교 사진)

# TODO
# 홈페이지 (로그인) -> 로그인 페이지(회원가입 버튼) 1) 로그인 완료 -> 홈페이지, 2) 회원가입 버튼 -> 회원가입 페이지
# 회원가입 로직(이메일 인증, 위치 받기- 동네 인증) 보안관련 어떤 게 있는지 공부도 해야하고
# 마이페이지
# 마이채팅방 리스트

# 다음 회의까지 구현은 말고 홈페이지를 맡았다 그럼 페이지가 어떻게 구성되는지 어떤 버튼이 들어가고(어떤 url을 연결시키고), 구상을 먼저 하고 해야 안 허버버
# 어떤 함수(로직)이 들어가야할까
# 시간이 좀 남는다. 이걸 구현하려면 어떤 기술?이 필요할까 (이메일 인증을 할건데 그럼 서버에서 인증 이메일은 어떻게 보내지?)

# 분배 - 사다리타기가 있구요 장단
# 1 홈페이지 (로그인) -> 로그인 페이지(회원가입 버튼) 1) 로그인 완료 -> 홈페이지, 2) 회원가입 버튼 -> 회원가입 페이지
# 2 회원가입 로직(이메일 인증, 위치 받기- 동네 인증) 보안관련 어떤 게 있는지 공부도 해야하고

# 장
# 1. 좀 더 쉽다.
# 2. 재밌다. (SMTP 이메일 프로토콜이 어떻게 동작하나 이런 재밌는 걸 배울 수 있다)

# 단
# 1. 어디서나 다 할 수 있고 해야하는 기본이다
# 2. 좀 더 어렵다.

# 1: 지원 유진
# 2: 수현 인찬