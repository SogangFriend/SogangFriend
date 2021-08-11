from django.db import models


# ex) Location : 서울특별시 마포구 대흥동
#               Do - null
#               Si - Seoul
#                   do = null
#                   isGYorTB = true
#               Gu - Mapo
#               Dong - Daeheung


class Do(models.Model):
    name = models.CharField(max_length=30, null=False)


class Si(models.Model):
    name = models.CharField(max_length=30, null=False)
    do = models.ForeignKey(Do, on_delete=models.CASCADE, null=True, blank=True)
    isGYorTB = models.BooleanField(default=False)


class Gu(models.Model):
    name = models.CharField(max_length=30, null=False)
    si = models.ForeignKey(Si, on_delete=models.CASCADE, null=True, blank=True)


class Dong(models.Model):
    name = models.CharField(max_length=30, null=False)
    gu = models.ForeignKey(Gu, on_delete=models.CASCADE, null=True, blank=True)


class Location(models.Model):
    do = models.ForeignKey(Do, on_delete=models.CASCADE, null=True, blank=True)
    si = models.ForeignKey(Si, on_delete=models.CASCADE, null=False)
    gu = models.ForeignKey(Gu, on_delete=models.CASCADE, null=True, blank=True)
    dong = models.ForeignKey(Dong, on_delete=models.CASCADE, null=True, blank=True)


class Member(models.Model):
    name = models.CharField(max_length=30, blank=False)  # blank랑 null차이? -> blank는 DB에 '' 로 저장됨, null은 열 자체에 값이 없음
    student_number = models.IntegerField(blank=True, null=True)  # choices(select박스) -> 폼에서 설정합니다!
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=10, blank=False)
    introduction = models.TextField(blank=True)  # help_text(필드입력도움말기능) -> 폼에서 설정합니당!
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False)
