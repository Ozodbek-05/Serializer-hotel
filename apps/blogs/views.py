from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.blogs.models import Post
from apps.blogs.serializers import RegisterSerializer, CategorySerializer, PostSerializer
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

@api_view(["GET","POST"])
def post_detail_view(request):
    post_id = request.data.get("id")
    if not post_id:
        return Response({"error": "Post id is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        post = Post.objects.get(id=post_id)
        if post.status != 'published' and post.author != request.user:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, context={'request': request})
    data = serializer.data
    if data is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(data)