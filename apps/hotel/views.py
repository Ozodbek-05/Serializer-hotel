from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.hotel.models import CustomUser, Room
from apps.hotel.serializer import RegisterSerializer, HotelsSerializer, RoomDetailSerializer, RoomSerializer, RoomsBookingsSerializer


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

    return None



@api_view(["GET", "POST", "PATCH"])
def rooms_bookings_view(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({"errors": "Room not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user if request.user.is_authenticated else CustomUser.objects.first()
    
    serializer = RoomsBookingsSerializer(
        data=request.data,
        context={"user": user, "room": room}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def room_detail_view(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

    serializer = RoomDetailSerializer(room)
    return Response(serializer.data)
