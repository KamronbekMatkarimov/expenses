from django.urls import path
from .views import MonthlyReportView

urlpatterns = [
    path('', MonthlyReportView.as_view(), name='monthly-report'),
]