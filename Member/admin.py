from django.contrib import admin
from .models import Member


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(Member, UserAdmin)
