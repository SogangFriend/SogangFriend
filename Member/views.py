from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, resolve_url

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


User = get_user_model()


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
            })
        )


def activate(request, uid64):#계정활성화 함수
    try:
        uid = force_text(urlsafe_base64_decode(uid64)) #decode해서 user 불러옴
        user = Member.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None
    if user is not None: #유효성 검사
        user.is_active = True
        user.save()
        return redirect('/login')

    else: #이메일 인증 기한 지남
        return render(request, "Member/register.html")


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
        introduction = request.POST.get('introduction', '')

        error_message = None
        if not (name and email and password and re_password and location and introduction):
            error_message = "필수문항(*)을 입력해 주세요."
        elif password != re_password:
            error_message = '비밀번호가 다릅니다.'
        elif not (email.endswith('@sogang.ac.kr') or email.endswith('@u.sogang.ac.kr')):
            error_message = '서강대학교 이메일을 사용해주세요.'
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

            user = User.objects.create_user(email=email, name=name, password=password, student_number=student_number,
                                            loc=loc, introduction=introduction)

            user.save()
            mail_send(user, request, False)
            return HttpResponse("회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.")
        return render(request, 'Member/register.html', {'error': error_message})  # register를 요청받으면 register.html 로 응답.


class LoginView(View):
    response_data = {}
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class()
        return render(request, 'Member/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            login_email = form.cleaned_data['email']
            login_password = form.cleaned_data['password']
            member = authenticate(email=login_email, password=login_password)
            if member is not None:
                login(request, member)
                request.session['member'] = member.pk
                return redirect('/')
            else:
                self.response_data['error'] = "비밀번호를 틀렸습니다."
        else:
            self.response_data['error'] = "이메일과 비밀번호를 모두 입력해주세요."
        return render(request, 'Member/login.html', self.response_data)


def log_out(request):
    logout(request)
    return redirect('/')


class MyPageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/member/mypage/'

    form_class = EditProfileView

    def get(self, request):
        member_pk = request.session['member']
        member = Member.objects.get(pk=member_pk)
        form = self.form_class(initial={'name': member.name, 'email': member.email,
                                        'password': member.password, 'introduction': member.introduction,
                                        'location': member.location.si.name + " " + member.location.gu.name + " " +
                                                    member.location.dong.name})
        return render(request, 'Member/my_page.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            member_pk = request.session['member']
            target_member = Member.objects.get(pk=member_pk)
            target_member.name = name
            target_member.introduction = introduction
            target_member.save()
        return redirect('/member/mypage/')


class PasswordChangeView(View):
    form_class = PasswordResetForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'Member/password_new_form.html', {'form': form})


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
                request.session['member'] = target_member.pk
            return render(request, 'Member/password_new_form.html', {'form': form})
        else:
            member_pk = request.session['member']
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
                request.session['member'] = member_pk
                form = PasswordResetForm()
                return render(request, 'Member/password_new_form.html',
                              {'form': form, 'error': "비밀번호가 일치하지 않습니다. 다시 입력해주세요."})


class MemberListView(View):
    def get(self,request):
        members = Member.objects.all()
        return render(request, 'Member/member_list.html', {"members":members})


class RetryMailView(View):
    def get(self, request, email):
        member = Member.objects.get(email=email)
        mail_send(member, request, False)
        return HttpResponse("회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.")

    