<<<<<<< Updated upstream
from django.shortcuts import render
=======
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import *
from Member.models import *

>>>>>>> Stashed changes

# Create your views here.

# 컨트롤러 역할
<<<<<<< Updated upstream
=======


class HomeView(View):
    def get(self, request):
        member_id = request.session.get('Member')
        if member_id:
            member_info = Member.objects.get(pk=member_id)  # pk : primary key
            return render(request, "homepage.html", {'member_info': member_info})  # 로그인을 했다면, home 출력
        return HttpResponse('로그인을 해주세요.')  # session에 member가 없다면, (로그인을 안했다면)

>>>>>>> Stashed changes
