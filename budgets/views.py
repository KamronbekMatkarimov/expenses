# budgets/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Budget
from .serializers import BudgetSerializer
from .filters import BudgetFilter
from expenses.permissions import IsAuthenticatedAndNotAnalystWrite


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticatedAndNotAnalystWrite]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BudgetFilter
    ordering_fields = ["month", "amount"]
    ordering = ["-month"]

    def get_queryset(self):
        user = self.request.user
        qs = Budget.objects.select_related("category")

        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
