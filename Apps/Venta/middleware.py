

class ValidarCuenta():

    def process_request(self, request):
        if request.user.is_authenticated():
            if request.session.get('cuenta') is None:
                request.session['cuenta'] = list()
