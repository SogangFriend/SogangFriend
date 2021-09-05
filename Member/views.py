from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

from .helper import send_mail
from django.views.generic import *
from .models import Member
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import *
from django.contrib.auth.hashers import make_password
from mainApp.models import *
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages, auth
from .tokens import account_activation_token
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMultiAlternatives
from django import template

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




def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('')
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "Member/change_pw.html",context)

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url=reverse_lazy('login')
    template_name = 'member/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordResetView(PasswordResetView):
    template_name = 'member/password_reset_form.html'
    email_template_name = 'member/password_reset_email.html'
    mail_title="비밀번호 재설정"

    def password_reset_request(request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        htmltemp = template.loader.get_template('member/password_reset_email.html')
                        c = {
                            "email":user.email,
                            'domain':'127.0.0.1:8000',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        html_content = htmltemp.render(c)
                        try:
                            msg = EmailMultiAlternatives(subject, text_content, 'Website <admin@example.com>', [user.email], headers = {'Reply-To': 'admin@example.com'})
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        messages.info(request, "Password reset instructions have been sent to the email address entered.")

                        return redirect ("password_reset_done")
        password_reset_form = change_pw(request)

        return render(request=request, template_name="Member/password_reset.html", context={"password_reset_form":change_pw(request)})




