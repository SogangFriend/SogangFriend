from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import MemberChangeForm, MemberCreationForm
from .models import *


# Register your models here.
class UserCustomAdmin(UserAdmin):
    form = MemberChangeForm
    add_form = MemberCreationForm

    list_display = ('email', 'name', 'student_number', 'location', 'introduction', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('name', 'student_number', 'location', 'introduction')}),
        ('권한', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        ('기본 정보', {'fields': ('email', 'password1', 'password2')}),
        ('추가 정보', {'fields': ('name', 'student_number', 'location', 'introduction')})
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Member, UserCustomAdmin)
admin.site.unregister(Group)
