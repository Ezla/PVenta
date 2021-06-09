from django.contrib import admin

from .models import Listed


class ListedAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'type', 'active')
    ordering = ('name',)


admin.site.register(Listed, ListedAdmin)
