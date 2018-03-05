from django.urls import reverse_lazy


def menu(request):
    return {'status_bar': request.session.get('status_bar')}
