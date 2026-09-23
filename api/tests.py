from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Event, Ticket


class TicketReservationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.event = Event.objects.create(
            name="Test Event",
            event_time="2026-10-15T18:00:00Z",
            venue="Lahore",
            ticket_capicity=1,
            available_ticket_count=1,
        )

    def test_cannot_overbook_event(self):
        url = reverse(
            "reserve-ticket",
            kwargs={"event_id": self.event.id}
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ticket.objects.count(), 1)

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_ticket_count, 0)

    def test_cannot_scan_ticket_twice(self):
        ticket = Ticket.objects.create(
            event=self.event,
            user=self.user,
            status="BOOKED",
        )

        url = reverse("scan-ticket")

        data = {
            "token_value": str(ticket.token_value)
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)

        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "USED")

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)

        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "USED")