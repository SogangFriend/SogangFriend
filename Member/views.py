from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, resolve_url
from django.urls import reverse_lazy

from .helpers import send_mail, email_auth_num
from django.views.generic import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import *
from django.http import HttpResponse
from MainApp.models import *
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from django.shortcuts import render

User = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


def mail_send(member, request, find):
    if find:
        auth_num = email_auth_num()
        send_mail(
            "{}님, 서강프렌드 비밀번호 재설정 메일입니다.".format(member.name), [member.email],
            html=render_to_string('password_reset_mail.html', {
                "user": member,
                "uid": urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),
                "domain": request.META['HTTP_HOST'],
                "auth_num": auth_num
            })
        )
        return auth_num
    else:
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
        return redirect('/member/login')

    elif user is None: #이메일 인증 기한 지남
        return render(request, "Member/register.html")
    else: #이미 확인된 토큰 혹은 유효기간이 지난 토큰
        #return HttpResponse("invalid")

        # return render(request, 'Member/login.html')
        return redirect('/member/login')


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
            s = Si.objects.filter(name=location_info[0])
            if s.count() != 0: # 이미 있으면
                s = s[0]
            else:
                s = Si(name=location_info[0], isGYorTB=True)  # 수정 필요 나중에 특별시 광역시 검사 로직 이거 지금 생성자
                s.save()
            g = Gu.objects.filter(name=location_info[1])
            if g.count() != 0:
                g = g[0]
            else:
                g = Gu(name=location_info[1], si=s)
                g.save()
            d = Dong.objects.filter(name=location_info[2])
            if d.count() != 0:
                d = d[0]
            else:
                d = Dong(name=location_info[2], si=s, gu=g)
                d.save()
            loc = Location.objects.filter(si=s, gu=g, dong=d)
            if loc.count() != 0:
                loc = loc[0]
            else:
                loc = Location(si=s, gu=g, dong=d)
                loc.save()

            user = User.objects.create_user(email=email, name=name, password=password, student_number=student_number, loc=loc, introduction=introduction)

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
                login(request, member)
                request.session['Member'] = member.pk
                return redirect('/')
            else:
                self.response_data['error'] = "비밀번호를 틀렸습니다."
        else:
            self.response_data['error'] = "이메일과 비밀번호를 모두 입력해주세요."
        return render(request, 'Member/login.html', self.response_data)


def log_out(request):
    logout(request)
    # request.session.pop('Member')
    return redirect('/')


class ProfileView(LoginRequiredMixin, View):
    login_url = '/member/login/'
    redirect_field_name = '/profle/'

    def get(self, request):
        member_pk = request.session.get('Member')
        member = Member.objects.get(pk=member_pk)
        return render(request, 'Member/profile.html', {'member': member})


class PasswordResetView(View):
    def get(self, request):
        form = EmailForm()
        return render(request, 'Member/password_email_form.html', {'form': form})

    def post(self, request):
        flag = request.POST.get('flag', 'new_password')
        if flag == "email":
            email = request.POST.get('email')
            member = Member.objects.filter(email=email)
            if member.count() == 0:
                form = EmailForm()
                return render(request, 'Member/password_email_form.html',
                              {'form': form,
                               'error': "해당하는 이메일이 없습니다.\n다시 입력해주세요."})

            else:
                form = AuthNumForm()
                auth_num = mail_send(member[0], request, True)
                return render(request, 'Member/password_auth_form.html',
                              {'form': form, 'auth_num': auth_num, 'email': email})
        elif flag == "auth_num":
            email = request.POST.get('email')
            generated = request.POST.get('generated_auth_num')
            input_num = request.POST.get('auth_num')
            if generated != input_num:
                form = EmailForm()
                return render(request, 'Member/password_email_form.html',
                              {'form': form,
                               'error': "인증번호가 다릅니다."})
            else:
                target_member = Member.objects.get(email=email)
                form = PasswordResetForm(target_member)
                request.session['auth'] = target_member.pk
            return render(request, 'Member/password_new_form.html', {'form': form})
        else:
            member_pk = request.session['auth']
            member = Member.objects.get(pk=member_pk)
            login(request, member)
            form = PasswordResetForm(member, request.POST)

            if form.is_valid():
                form.save()
                message = "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요."
                logout(request)
                return render(request, "Member/password_reset_done.html", {"message": message})
            else:
                logout(request)
                request.session['auth'] = member_pk
                form = PasswordResetForm()
                return render(request, 'Member/password_new_form.html',
                              {'form': form, 'error': "비밀번호가 일치하지 않습니다. 다시 입력해주세요."})


