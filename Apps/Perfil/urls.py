from django.conf.urls import url

from .views import ListPerfilUsuario, EditUser, CreateUser, EditPass

app_name = 'PerfilUsuario'
urlpatterns = [
    url(r'^Usuario/Lista/$', ListPerfilUsuario.as_view(), name='url_lista'),
    url(r'^Usuario/Actualizar/(?P<pk>\d+)/$', EditUser.as_view(),
        name='url_actualizar'),
    url(r'^Usuario/Nuevo/$', CreateUser.as_view(), name='url_nuevo'),
    url(r'^Usuario/Cambiar/Passdord/(?P<pk>\d+)/$', EditPass.as_view(),
        name='url_up_pass'),
]
