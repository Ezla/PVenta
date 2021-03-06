from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SalesAccountSerialiser, SalesProductSerialiser, \
    SalesCartSerialiser, ChangeProductSerialiser
from .models import Discount
from .utils import process_cart
from Apps.Producto.models import Producto


class SearchProductView(APIView):

    def post(self, request):
        word = request.data.get('word', str())
        try:
            products = request.session.get('account', list())
            query = Producto.objects.get(codigo=word)
            # Agregamos producto encontrado a la cuenta
            product_exist = False
            for product in products:
                if product.get('code') == query.codigo:
                    product_exist = True
                    new_quantity = Decimal(
                        product.get('quantity')) + Decimal(1)
                    product['quantity'] = new_quantity
                    break
            if not product_exist:
                price = query.punitario
                product = {'code': query.codigo,
                           'name': query.descripcion,
                           'with_discount': False,
                           'price': price,
                           'price_up': query.punitario,
                           'price_down': query.pmayoreo,
                           'quantity': Decimal(1),
                           'sales_account': None}
                products.insert(0, product)
            sales = SalesProductSerialiser(data=products, many=True)
            if sales.is_valid():
                request.session['account'] = sales.data
                return Response(sales.data, status=status.HTTP_200_OK)
            else:
                return Response(sales.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            suggestions = self.get_suggestions(word=word)
            return Response(suggestions, status=status.HTTP_202_ACCEPTED)

    def get_suggestions(self, word):
        suggestions = list()
        if word:
            query = Producto.objects.filter(descripcion__icontains=word)
            for product in query:
                suggestions.append(
                    {'code': product.codigo, 'name': product.descripcion,
                     'brand': product.marca.marca,
                     'price': str(product.punitario)})
        return suggestions


class SalesProductChangeView(APIView):

    def post(self, request):
        products = request.session.get('account', list())
        change_product = ChangeProductSerialiser(data=request.data)

        if not change_product.is_valid():
            return Response(change_product.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        code = change_product.validated_data.get('code')
        quantity = change_product.validated_data.get('quantity')
        with_discount = change_product.validated_data.get('with_discount')

        # Actualizamos data
        product_exists = False
        for product in products:
            product_exists = product.get('code') == code
            if product_exists and quantity >= Decimal(0.5):
                product['quantity'] = quantity
                product['with_discount'] = with_discount
                break
            elif product_exists:
                products.remove(product)
                break
        # respondemos un 404 si no se encuentra el producto
        if not product_exists:
            return Response({'code', 'El producto no esta en el carrito.'},
                            status=status.HTTP_404_NOT_FOUND)
        sales = SalesProductSerialiser(data=products, many=True)
        if sales.is_valid():
            request.session['account'] = sales.data
            return Response(sales.data, status=status.HTTP_200_OK)
        # respondemos un 400 si la data no es valida
        return Response(sales.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesCartStatusView(APIView):

    def get(self, request):
        cart = request.session.get('account', list())
        percent_off = request.GET.get('percent_off', 0)
        subtotal, total, discount = process_cart(cart=cart,
                                                 percent_off=percent_off)
        data = {'subtotal': subtotal, 'total': total, 'discount': discount}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        request.session['account'] = list()
        return Response({}, status=status.HTTP_200_OK)


class AccountView(APIView):

    def post(self, request):
        cart = request.session.get('account', list())
        percentage = request.data.get('percent_off')
        cash = Decimal(request.data.get('cash'))
        percent_off = get_object_or_404(Discount, percentage=percentage)

        percentage = percent_off.percentage
        subtotal, total, discount = process_cart(cart=cart,
                                                 percent_off=percentage)
        change_due = cash - total
        data = {'subtotal': subtotal, 'total': total, 'cash': cash,
                'change_due': change_due, 'discount': percent_off.pk}
        account = SalesAccountSerialiser(data=data)
        sales = SalesProductSerialiser(data=cart, many=True)

        if account.is_valid() and sales.is_valid():
            # guardamos cuenta
            sales_account = account.save()
            cart = sales.data
            # agregamos la id de la cuenta a los productos en cart
            for product in cart:
                product.update({'sales_account': sales_account.pk})
            # guardamos productos de la venta
            new_sales = SalesCartSerialiser(data=cart, many=True)
            if new_sales.is_valid():
                new_sales.save()
            request.session['account'] = list()
            return Response(account.data, status=status.HTTP_201_CREATED)
        return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)
