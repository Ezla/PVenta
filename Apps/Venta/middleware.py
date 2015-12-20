

class ValidarCuenta():

    def process_request(self, request):
        if request.user.is_authenticated():
            if request.session.get('cuenta') is None:
                request.session['cuenta'] = list()
            if request.session.get('status_bar') is None:
                request.session['status_bar'] = ''
            if request.session.get('notificaciones') is None:
                request.session['notificaciones'] = list()
            if request.session.get('song') is None:
                request.session['song'] = False
            if request.session.get('visto') is None:
                request.session['visto'] = False
            if request.session.get('cantidad') is None:
                request.session['cantidad'] = 0
