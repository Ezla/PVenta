from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ListedSerialiser
from .models import Listed


class ApiListedView(APIView):

    def get(self, request):
        query = Listed.objects.all().order_by('name')
        listed = ListedSerialiser(query, many=True)

        return Response(listed.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ListedSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ApiEnumerateListingView(APIView):

    def get(self, request):
        query = Listed.objects.all().order_by('name')
        count = 0
        for item in query:
            count += 1
            item.number = count
            item.save()
        listed = ListedSerialiser(query, many=True)
        return Response(listed.data, status=status.HTTP_200_OK)
