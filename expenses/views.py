from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer
from .filters import ExpenseFilter
from .permissions import IsAuthenticatedAndNotAnalystWrite


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedAndNotAnalystWrite]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ["description"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user
        qs = Expense.objects.select_related("category")

        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedAndNotAnalystWrite]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user
        qs = Category.objects.all()
        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": "Нельзя удалить категорию, у которой есть расходы",
                        "details": None,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)