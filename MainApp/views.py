from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, request
from django.views.generic import *
from Member.models import *
from SGFriend.settings import STATICFILES_DIRS
import json
# Create your views here.

# 컨트롤러 역할


class HomeView(LoginRequiredMixin, View):
    login_url = '/member/login/'
    redirect_field_name = '/'

    def get(self, request):
        member_id = request.session.get('Member')
        member_info = Member.objects.get(pk=member_id)  # pk : primary key
        # 서울특별시 금천구
        # 강원도 강릉시
        file_path = STATICFILES_DIRS[0] + "/gsons/"

        if member_info.location.si.isGYorTB:
            file_path += member_info.location.si.name + "/" + member_info.location.gu.name + ".geojson"
        else :
            file_path += member_info.location.do.name + "/" + member_info.location.si.name + ".geojson"
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        return render(request, "homepage.html",
                      {'member_info': member_info, 'json_data': json_data})  # 로그인을 했다면, home 출력

# render <-> redirect
# render는 html을 뿌려주는거고
# redirect는 다시 그 url -> 뷰로


class MemberListView(LoginRequiredMixin, View):
    login_url = '/member/login/'
    redirect_field_name = '/'

    def get(self, request):
        member_id = request.session.get('Member')
        member_info = Member.objects.get(pk=member_id)
        members = Member.objects.filter(location=member_info.location)
        return render(request, "member_list.html",
                      {"members": members})
