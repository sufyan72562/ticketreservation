import uuid

from django.db import models
from django.contrib.auth.models import User
from api.constants import STATUS_CHOICES
from datetime import datetime
import secrets


class Event(models.Model):
    name = models.CharField(max_length=50)
    event_time = models.DateTimeField()
    venue = models.CharField(max_length=100)
    ticket_capicity = models.IntegerField(default=0)
    available_ticket_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.available_ticket_count = self.ticket_capicity

        super().save(*args, **kwargs)


class Ticket(models.Model):
    ticket_id = models.CharField(unique=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="ticket")
    status = models.CharField(choices=STATUS_CHOICES, default="Pending", max_length=20)
    token_value = models.UUIDField(default=uuid.uuid4, unique=True)
    reservation_date = models.DateField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="ticket")

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = secrets.token_hex(6).upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.ticket_id)