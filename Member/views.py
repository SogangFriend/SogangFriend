from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import *
from .models import Member
from .helpers import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
# Create your views here.


class MailView(View):
    def get(self, request):
        member = Member.objects.get(email='dls4585@naver.com')
        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(member.name),
            [member.email],
            html=render_to_string('send_mail.html', {
                'user': member,
                'uid': urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),
                'domain': request.META['HTTP_HOST'],
                # 'token': default_token_generator.make_token(member),
            })
        )
        return render(request, 'send_mail.html', {})

