from django.http import Http404
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

class ApiListedDetailView(APIView):
    """
    Retrieve, update or delete a Listed instance.
    """
    def get_object(self, pk):
        try:
            return Listed.objects.get(pk=pk)
        except Listed.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        listed = self.get_object(pk)
        serializer = ListedSerialiser(listed)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        listed = self.get_object(pk)
        serializer = ListedSerialiser(listed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        listed = self.get_object(pk)
        listed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
