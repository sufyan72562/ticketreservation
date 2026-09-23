from django.urls import path
from .views import ReserveTicketView, UserCreateView, UserListView, UserDetailView, EventsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view()),
    path("users/register/", UserCreateView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("events/", EventsView.as_view()),
    path("events/tickets/", ReserveTicketView.as_view()),
    path("events/<int:event_id>/reserve/", ReserveTicketView.as_view()),
]