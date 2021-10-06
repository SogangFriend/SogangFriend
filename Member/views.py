from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetView
from django.shortcuts import render, redirect, reverse, resolve_url
from django.urls import reverse_lazy

from .helpers import send_mail
from django.views.generic import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import *
from django.http import HttpResponse
from mainApp.models import *
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

        # return render(request, 'Member/login.html')
        return redirect(request, 'Member/login')


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

#password change
class UserPasswordResetView(PasswordResetView):
    template_name = 'Member/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('Member:password_reset_done')
    form_class = PasswordResetForm
    email_template_name= 'Member/password_reset_email.html'
    subject_template_name= 'Member/password_reset_subject.txt'

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'Member/password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'Member/password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력


class MySetPasswordForm(SetPasswordForm):
    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True
        if commit:
            user.save()
        return user


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url=reverse_lazy('Member:password_reset_complete')
    template_name = 'Member/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'Member/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('Member:login')
        return context


class ProfileView(LoginRequiredMixin, View):
    login_url = '/member/login/'
    redirect_field_name = '/profle/'

    def get(self, request):
        member_pk = request.session.get('Member')
        member = Member.objects.get(pk=member_pk)
        return render(request, 'Member/profile.html', {'member': member})