from django.shortcuts import render, redirect, reverse
from .helper import send_mail
from django.views.generic import *
from .models import Member
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from mainApp.models import *
from django.utils.encoding import force_bytes, force_text
from django.forms import ValidationError
from django.contrib import messages
from .tokens import account_activation_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

User = get_user_model()


def mail_send(member, request, find):
    send_mail(
        "{}님의 회원가입 인증 메일입니다.".format(member.name), [member.email],
        html=render_to_string('send_mail.html', {
            "user": member,
            'uid': urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),#pk를 자연수에서 bytes로 변환,인코드, bytes에서 str로 변환
            'domain': request.META['HTTP_HOST'],
            'token': account_activation_token.make_token(member),#token.py에서 만들었던 token 생성기로 token생성
        })
    )

def activate(request, uid64, token):#계정활성화 함수
    try:
        uid = force_text(urlsafe_base64_decode(uid64)) #decode해서 user 불러옴
        user = Member.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): #유효성 검사
        user.is_active = True
        user.save()
        #return render(request, "homepage.html") #~님 환영합니다?
        return render(request, "test2.html")
    elif user is None: #이메일 인증 기한 지남
        return render(request, "Member/register.html")
    else: #이미 확인된 토큰 혹은 유효기간이 지난 토큰
        #return HttpResponse("invalid")

        return render(request, 'Member/login.html')


class RegisterView(APIView):
    def get(self, request):
        return render(request, 'Member/register.html')

      
    def post(self, request):
        name = request.POST.get('name', '')
        student_number = request.POST.get('student_number', '')
        email = request.POST.get('email', '')
        location = request.POST.get('location', '')
        password = request.POST.get('password', '')
        re_password = request.POST.get('re_password', '')
        introduction = request.POST.get('introduction', '')

        res_data = {}
        if not (name and email and password and re_password and location and introduction):
            # return HttpResponse('필수문항(*)을 입력해 주세요.')
            res_data['error'] = "필수문항(*)을 입력해 주세요."
        if password != re_password:
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'

        else:
            location_info = str(location).split(' ')
            # 수정 필요 이미 있는지 검사
            si = Si(name=location_info[0], isGYorTB=True)  # 수정 필요 나중에 특별시 광역시 검사 로직
            si.save()
            gu = Gu(name=location_info[1], si=si)
            gu.save()
            dong = Dong(name=location_info[2], si=si, gu=gu)
            dong.save()
            loc = Location(si=si, gu=gu, dong=dong)
            loc.save()

            user = User.objects.create_user(email=email, name=name, password=password, student_number=student_number,
                                            loc=loc, introduction=introduction)
            user.save()
            mail_send(user, request, False)
            token = Token.objects.create(user=user)
            return HttpResponse("회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.")
        return render(request, 'Member/register.html', res_data)  # register를 요청받으면 register.html 로 응답.


class LoginView(View):
    response_data = {}
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'Member/login.html', {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            login_email = form.cleaned_data['email']
            login_password = form.cleaned_data['password']
            member = authenticate(email=login_email, password=login_password)
            if member is not None:
                token = Token.objects.get(user=member)
                Response({"Token": token.key})
                return redirect('/')

            else:
                self.response_data['error'] = "비밀번호를 틀렸습니다."
        else:
            self.response_data['error'] = "이메일과 비밀번호를 모두 입력해주세요."
        return render(request, 'Member/login.html', self.response_data)


def logout(request):
    request.session.pop('Member')
    return redirect('/')
