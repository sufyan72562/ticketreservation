from api.models import Event, Ticket
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

class EventService:
    def get_event_by_id(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return None

    def get_all_events(self):
        return Event.objects.all()


class TicketService:
    def reserve_ticket(self, event_id, user):
        with transaction.atomic():
            if not Event.objects.filter(id=event_id).exists():
                raise ValidationError(
                    "Event does not exist."
                )

            updated = Event.objects.filter(id=event_id, 
                                    available_ticket_count__gt=0).update(
                                        available_ticket_count=F('available_ticket_count') - 1)

            if updated == 0:
                raise ValidationError("No available tickets for this event.")

            ticket = Ticket.objects.create(
                event_id=event_id,
                user=user,
                status="BOOKED"
            )
            return ticket
        
       
      
        



    