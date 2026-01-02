from django.urls import path
from .views import dashboard

app_name = "finances"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]