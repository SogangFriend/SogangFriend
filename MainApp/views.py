from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from Member.models import *
from django.core.cache import cache
# Create your views here.

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

        if member_info.location.si.isGYorTB:
            key += "_" + member_info.location.gu.name
        else:
            key = member_info.location.do.name + "_" + key

        coords = cache.get(key)
        return render(request, "homepage.html",
                      {'member_info': member_info, 'json_data': {'location': coords}, 'members': members})  # 로그인을 했다면, home 출력


# render <-> redirect
# render는 html을 뿌려주는거고
# redirect는 다시 그 url -> 뷰로
