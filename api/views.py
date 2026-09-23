from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer, EventSerializer, TicketSerializer
from api.services import EventService, TicketService

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



class EventsView(generics.ListAPIView):
    queryset = EventService().get_all_events()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class ReserveTicketView(generics.GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        user = request.user
        ticket = TicketService().reserve_ticket(event_id, user)
        serializer = self.get_serializer(ticket)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
        

