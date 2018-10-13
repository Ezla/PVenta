from django.urls import path

from .views import ListedView

app_name = 'varios'
urlpatterns = [
    path('listed/', ListedView.as_view(), name='url_listed'),
]
