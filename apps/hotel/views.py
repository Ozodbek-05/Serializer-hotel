from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.hotel.models import Room
from apps.hotel.serializer import RegisterSerializer, HotelsSerializer, RoomSerializer


@api_view(["GET", "POST"])
def user_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","POST"])
def hotels_view(request):
    serializer = HotelsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def rooms_view(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH"])
def rooms_id_view(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def rooms_bookings_view(request,pk):
    pass