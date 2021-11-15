import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from Member.models import *
from django.core.cache import cache
# Create your views here.
from SGFriend.settings import STATICFILES_DIRS


# 컨트롤러 역할


class HomeView(LoginRequiredMixin, View):
    login_url = '/member/login/'
    redirect_field_name = '/'

    def get(self, request):
        member_id = request.session.get('Member')
        member_info = Member.objects.get(pk=member_id)  # pk : primary key
        members = Member.objects.filter(location=member_info.location)

        # 서울특별시 금천구
        # 강원도 강릉시
        key = member_info.location.si.name
        path = STATICFILES_DIRS[0] + "/gsons/"
        if member_info.location.si.isGYorTB:
            key += "_" + member_info.location.gu.name
            path += member_info.location.si.name + "/" + member_info.location.gu.name + ".geojson"
        else:
            key = member_info.location.do.name + "_" + key
            path += member_info.location.do.name + "/" + member_info.location.si.name + ".geojson"

        coords = []
        if not cache.get(key):
            with open(path, "r") as f:
                json_data = json.load(f)
                features = json_data['features']
                for feature in features:
                    data = {
                        'name': feature['properties']['adm_nm'].split()[2],
                        'coords': feature['geometry']['coordinates']
                    }
                    coords.append(data)
                cache.set(key, coords)
            data = {'location': coords}
        else:
            data = {'location': cache.get(key)}

        return render(request, "homepage.html",
                      {'member_info': member_info, 'json_data': data,
                       'members': members})  # 로그인을 했다면, home 출력

# render <-> redirect
# render는 html을 뿌려주는거고
# redirect는 다시 그 url -> 뷰로
