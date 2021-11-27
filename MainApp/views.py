import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from SGFriend.settings import STATICFILES_DIRS
import json
from Chat.models import *
from django.core.cache import cache
# Create your views here.


# 컨트롤러 역할


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def get(self, request):
        member_id = request.session.get('member')
        member_info = Member.objects.get(pk=member_id)  # pk : primary key
        members = Member.objects.filter(location=member_info.location)
        chats = ChatRoom.objects.filter(location=member_info.location)


        # 서울특별시 금천구
        # 강원도 강릉시
        key = member_info.location.si
        path = STATICFILES_DIRS[0] + "/gsons/"
        if member_info.location.isGYorTB:
            key += "_" + member_info.location.gu
            path += member_info.location.si + "/" + member_info.location.gu + ".geojson"

        else:
            key = member_info.location.do + "_" + key
            path += member_info.location.do + "/" + member_info.location.si + ".geojson"

        coords = []
        if not cache.get(key):
            with open(path, "r", encoding="UTF-8") as f:
                json_data = json.load(f)
                features = json_data['features']
                for feature in features:
                    data = {
                        'name': feature['properties']['adm_nm'],
                        'coords': feature['geometry']['coordinates']
                    }
                    coords.append(data)
                cache.set(key, coords)
            data = {'location': coords}
        else:
            data = {'location': cache.get(key)}
        left = 100000.0; right = 0.0; top = 1000.0; bottom = 0.0
        for d in data['location']:
            for coords in d['coords']:
                for coordinate in coords[0]:
                    if coordinate[1] < top:
                        top = coordinate[1]
                    if coordinate[1] > bottom:
                        bottom = coordinate[1]
                    if coordinate[0] < left:
                        left = coordinate[0]
                    if coordinate[0] > right:
                        right = coordinate[0]
        midLat = (top + bottom) / 2
        midLng = (left + right) / 2
        center = {'lat': midLat, 'lng': midLng}

        return render(request, "homepage.html",
                      {'member_info': member_info, 'json_data': data,
                       'members': members,  'chats': chats, 'center': center})  # 로그인을 했다면, home 출력

# render <-> redirect
# render는 html을 뿌려주는거고
# redirect는 다시 그 url -> 뷰로
