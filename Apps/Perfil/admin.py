from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'plantilla', 'get_avatar')


admin.site.register(UserProfile, UserProfileAdmin)
