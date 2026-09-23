from api.models import Event, Ticket
from rest_framework.exceptions import ValidationError
from django.db import transaction

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
        try:
            with transaction.atomic():

                event = Event.objects.select_for_update().get(id=event_id)

                if event.available_ticket_count <= 0:
                    raise ValidationError("Event tickets are sold out!")
                event.available_ticket_count -= 1
                event.save(update_fields=["available_ticket_count"])

                ticket = Ticket.objects.create(
                    event=event,
                    user=user,
                    status="BOOKED"
                )
                return ticket
       
        except Event.DoesNotExist:
            raise ValidationError("Event not found.")
        
       
      
        



    