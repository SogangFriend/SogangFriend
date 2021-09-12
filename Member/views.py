from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordContextMixin
from django.core.serializers import json
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from .helper import send_mail
from .forms import *
from django.contrib.auth.hashers import make_password
from mainApp.models import *
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password

from .models     import Member
from .tokens     import account_activation_token

from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode

from django.utils.encoding          import force_bytes, force_text

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic, View
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm



def mail_authenticate(member, request):
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

class RegisterView(View):

    def get(self, request):
        return render(request, 'Member/register.html')

    def post(self, request):
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
            member = Member(name=name, student_number=student_number, email=email, password=make_password(password), location=loc)
            member.save()

            mail_authenticate(member, request)
            return HttpResponse("회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.")

        return render(request, 'Member/register.html', res_data)  # register를 요청받으면 register.html 로 응답.


class LoginView(View):
    response_data = {}
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'Member/login.html', {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            login_email = form.cleaned_data['email']
            login_password = form.cleaned_data['password']
            member = Member.objects.get(email=login_email)
            # db에서 꺼내는 명령. Post로 받아온 email으로 , db의 email을 꺼내온다.
            if check_password(login_password, member.password):
                request.session['Member'] = member.id
                # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                # 세션 member라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                self.response_data['error'] = "비밀번호를 틀렸습니다."
        else:
            self.response_data['error'] = "이메일과 비밀번호를 모두 입력해주세요."
        return render(request, 'Member/login.html', self.response_data)


def logout(request):
    request.session.pop('Member')
    return redirect('/')

class UserPasswordResetView(PasswordResetView):
    template_name = 'Member/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
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

# def change_pw(request):
#     context= {}
#     user = request.user
#     if check_password(user.password):
#             new_password = request.POST.get("password1")
#             password_confirm = request.POST.get("password2")
#             if new_password == password_confirm:
#                 user.set_password(new_password)
#                 user.save()
#                 auth.login(request,user)
#                 return redirect("account:home")
#             else:
#                 context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
#
#     return render(request, "member/change_pw.html",context)

UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'



class MySetPasswordForm(SetPasswordForm):

    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True
        if commit:
            user.save()
        return user

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url=reverse_lazy('password_reset_complete')
    template_name = 'Member/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'Member/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context



