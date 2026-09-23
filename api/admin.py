from django.contrib import admin
from api.models import Ticket, Event


admin.site.register(Ticket)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event_time",
        "venue",
        "ticket_capicity",
        "available_ticket_count",
    )

    readonly_fields = ("available_ticket_count",)

