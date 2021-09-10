from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import *
from Member.models import *
from SGFriend.settings import STATIC_ROOT
import json
# Create your views here.

# 컨트롤러 역할


class HomeView(View):
    def get(self, request):
        member_id = request.session.get('Member')
        if member_id:
            member_info = Member.objects.get(pk=member_id)  # pk : primary key
            file_path = STATIC_ROOT + "/gsons/"
            if member_info.location.do:
                file_path += member_info.location.do.name
            if member_info.location.gu:
                file_path += member_info.location.gu.name + ".geojson"
            with open(file_path, 'r') as f:
                json_data = json.load(f)
            return render(request, "homepage.html", {'member_info': member_info, 'json_data': json_data})  # 로그인을 했다면, home 출력
        return HttpResponse('로그인을 해주세요.')  # session에 member가 없다면, (로그인을 안했다면)

# render <-> redirect
# render는 html을 뿌려주는거고
# redirect는 다시 그 url -> 뷰로

