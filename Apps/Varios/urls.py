from django.urls import path

from .views import ListedView
from .api_views import ApiListedView

app_name = 'varios'
urlpatterns = [
    path('listed/', ListedView.as_view(), name='url_listed'),
    path('api/listed/', ApiListedView.as_view(), name='url_api_listed'),
]
