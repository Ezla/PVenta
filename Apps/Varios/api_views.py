from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ListedSerialiser
from .models import Listed


class ApiListedView(APIView):

    def get(self, request):
        query = Listed.objects.all()
        listed = ListedSerialiser(query, many=True)

        return Response(listed.data, status=status.HTTP_200_OK)
