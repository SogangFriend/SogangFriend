from django.db import models
from mainApp.models import *
# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=30, blank=False)  # blank랑 null차이? -> blank는 DB에 '' 로 저장됨, null은 열 자체에 값이 없음
    student_number = models.IntegerField(blank=True, null=True)  # choices(select박스) -> 폼에서 설정합니다!
    email = models.EmailField(blank=False) # 이메일 검증은 views.py 에서 저희가 로직을 만들어서 검증을 합니다
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    password = models.CharField(max_length=30, blank=False)
    # 알아봐야될거같은데 보안 때문에, 사용자가 패스워드로 123456 입력 -> 내부에 해쉬함수로 못알아보는 값으로 저장을 해야 돼요 -> 장고는 어떻게?
    introduction = models.TextField(blank=True, null=True)  # help_text(필드입력도움말기능) -> 폼에서 설정합니당!

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'test_user'