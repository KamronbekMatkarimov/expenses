from django.urls import path
from .views import MonthlyReportView, MonthlyReportEmailView

urlpatterns = [
    path("", MonthlyReportView.as_view(), name="monthly-report"),
    path("email/", MonthlyReportEmailView.as_view(), name="monthly-report-email"),
]
