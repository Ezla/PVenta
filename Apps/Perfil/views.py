from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView
from .models import UserProfile
from .forms import FormUserUp, FormCreateUser, FormEditPass
from django.contrib.auth.models import User
from Apps.Venta.views import LoginRequiredMixin


class ListPerfilUsuario(LoginRequiredMixin, ListView):
    template_name = 'Perfil/usuarios_list.html'
    paginate_by = 10
    model = User


class EditUser(LoginRequiredMixin, UpdateView):
    template_name = 'Perfil/form_user.html'
    form_class = FormUserUp
    success_url = reverse_lazy('PerfilUsuario:url_lista')
    model = User
    context_object_name = 'us'

    def form_valid(self, form):
        user = form.save()
        if self.request.FILES.get('avatar'):
            try:
                perfil = UserProfile.objects.get(user=user)
                perfil.avatar = self.request.FILES.get('avatar')
                perfil.save()
            except:
                UserProfile.objects.create(user=user,
                                           avatar=self.request.FILES.get(
                                               'avatar'))

        return HttpResponseRedirect(self.get_success_url())


class CreateUser(LoginRequiredMixin, FormView):
    template_name = 'Perfil/form_user_create.html'
    form_class = FormCreateUser
    success_url = reverse_lazy('PerfilUsuario:url_lista')
    model = User

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        user = User.objects.create_user(username=username, password=password)
        user.email = form.cleaned_data.get('email')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        UserProfile.objects.create(user=user,
                                   avatar=self.request.FILES.get('avatar'))
        return super(CreateUser, self).form_valid(form)


class EditPass(LoginRequiredMixin, UpdateView):
    template_name = 'Perfil/form_pass.html'
    form_class = FormEditPass
    success_url = reverse_lazy('Venta:url_index')
    model = User

    def form_valid(self, form):
        user = form.save()
        user.password = make_password(
            password=form.cleaned_data.get('password2'))
        user.save()
        return HttpResponseRedirect(self.get_success_url())
