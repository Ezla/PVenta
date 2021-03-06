class ValidarCuenta:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
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
            if request.session.get('descuento') is None:
                request.session['descuento'] = 0

        response = self.get_response(request)
        return response
