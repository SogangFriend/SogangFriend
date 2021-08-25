from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *


# Create your views here.
def register(request):  # 회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'Member/register.html')

    elif request.method == "POST":
        name = request.POST.get('name', '')
        student_number = request.POST.get('student_number', '')
        email = request.POST.get('email', '')
        location = request.POST.get('location', '')
        password = request.POST.get('password', '')
        re_password = request.POST.get('re_password', '')
        introduction = request.POST.get('email', '')
        res_data = {}

        if not (name and email and password and re_password and location and introduction):
            # return HttpResponse('필수문항(*)을 입력해 주세요.')
            res_data['error'] = "필수문항(*)을 입력해 주세요."
        if password != re_password:
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'

        else:
            member = Member(name=name, email=email, password=make_password(password))
            member.save()
        return render(request, 'Member/register.html', res_data)  # register를 요청받으면 register.html 로 응답.


def login(request):
    response_data = {}

    if request.method == "GET":
        return render(request, 'Member/login.html')

    elif request.method == "POST":
        login_email = request.POST.get('email', None)
        login_password = request.POST.get('password', None)

        if not (login_email and login_password):
            response_data['error'] = "이메일과 비밀번호를 모두 입력해주세요."
        else:
            member = Member.objects.get(email=login_email)
            # db에서 꺼내는 명령. Post로 받아온 email으로 , db의 email을 꺼내온다.
            if check_password(login_password, member.password):
                request.session['Member'] = member.id
                # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                # 세션 member라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'Member/login.html', response_data)


def home(request):
    member_id = request.session.get('Member')
    if member_id:
        member_info = Member.objects.get(pk=member_id)  # pk : primary key
        return HttpResponse('home')  # 로그인을 했다면, home 출력

    return HttpResponse('로그인을 해주세요.')  # session에 member가 없다면, (로그인을 안했다면)


def logout(request):
    request.session.pop('Member')
    return redirect('/')
