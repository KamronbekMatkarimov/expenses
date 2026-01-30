from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Budget
from .serializers import BudgetSerializer
from .filters import BudgetFilter


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BudgetFilter

    ordering_fields = ["month", "amount", "id"]
    ordering = ["-month", "-id"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Budget.objects.all()
        return Budget.objects.filter(user=user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({
                "non_field_errors": [
                    "Бюджет на эту категорию и месяц уже существует. Используй PATCH/PUT."
                ]
            })
