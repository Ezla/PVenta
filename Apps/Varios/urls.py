from django.urls import path

from .views import ListedView
from .api_views import ApiListedView, ApiEnumerateListingView

app_name = 'varios'
urlpatterns = [
    path('listed/', ListedView.as_view(), name='url_listed'),
    path('api/listed/', ApiListedView.as_view(), name='url_api_listed'),
    path('api/listed/enumerate/', ApiEnumerateListingView.as_view(),
         name='url_api_listed_enumerate'),
]
