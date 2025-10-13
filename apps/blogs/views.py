from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.blogs.serializers import RegisterSerializer, CategorySerializer
from apps.hotel.models import CustomUser


@api_view(['POST', 'GET'])
def user_register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return None

@api_view(["GET","POST"])
def category_view(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CategorySerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return None