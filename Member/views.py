from .helper import send_mail
from .forms import *
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import *
from Member.models import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template

def mail_send(member, request, find):
    if find:
        send_mail(
            "{}님의 회원가입 인증 메일입니다.".format(member.name), [member.email],
            html=render_to_string('send_mail.html', {
                "user": member,
                'uid': urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),
                'domain': request.META['HTTP_HOST'],
                # 'token': default_token_generator.make_token(self.object),
            })
        )
    else:
        send_mail(
            "{}님의 회원가입 인증 메일입니다.".format(member.name), [member.email],
            html=render_to_string('send_mail.html', {
                "user": member,
                'uid': urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),
                'domain': request.META['HTTP_HOST'],
                # 'token': default_token_generator.make_token(self.object),
            })
        )


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
            member = Member(name=name, student_number=student_number, email=email, password=make_password(password),
                            location=loc)
            member.save()
            mail_send(member, request)
            return HttpResponse("메일 확인 바람")
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


def password_reset_request(request, *args, **kwargs):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    plaintext = template.loader.get_template('member/password/password_reset_email.txt')
                    htmltemp = template.loader.get_template('member/password/password_reset_email.html')
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)).encode(),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'Website <sogangfriend@naver.com>', [user.email], headers = {'Reply-To': 'admin@example.com'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    #messages.info(request, "Password reset instructions have been sent to the email address entered.")
                    return redirect ('/member/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="member/password/password_reset_confirm.html", context={"password_reset_form":password_reset_form})