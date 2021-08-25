from django.shortcuts import render, redirect

# Create your views here.
from .helper import send_mail
from django.views.generic import *
from .models import Member
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail.message import EmailMessage
from .forms import *
from django.http import HttpResponse

class MailView(View):
    form_class = MailForm

    def get(self, request):
        form = self.form_class() #폼생성

        return render(request, 'form_test.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            member = Member.objects.get(email=email)
            send_mail(
                "{}님의 회원가입 인증 메일입니다.".format(member.name), [member.email],
                html=render_to_string('send_mail.html', {
                    "user": member,
                    'uid': urlsafe_base64_encode(force_bytes(member.pk)).encode().decode(),
                    'domain': request.META['HTTP_HOST'],
                    #'token': default_token_generator.make_token(self.object),
                })
            )
            return HttpResponse('mail sent')



