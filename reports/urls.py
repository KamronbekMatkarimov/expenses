from django.urls import path
from .views import ReportsView, ReportEmailView

urlpatterns = [
    path("reports/", ReportsView.as_view(), name="reports"),
    path("reports/email/", ReportEmailView.as_view(), name="reports-email"),
]
