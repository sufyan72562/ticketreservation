from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Event
from api.models import Ticket

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id", "name","event_time",
                   "available_ticket_count", "venue"]


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "ticket_id",
            "event",
            "user",
            "reservation_date",
            "status",
            "token_value",
        ]
        read_only_fields = [
            "ticket_id",
            "event",
            "user",
            "reservation_date",
            "status",
            "token_value",
        ]
