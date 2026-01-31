from django.urls import path
from .views import ReportsView, ReportEmailView

urlpatterns = [
    path("", ReportsView.as_view(), name="reports"),
    path("email/", ReportEmailView.as_view(), name="reports-email"),
]
