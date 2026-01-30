from django_filters import rest_framework as filters
from .models import Budget, normalize_month

class BudgetFilter(filters.FilterSet):
    month = filters.DateFilter(method="filter_month")

    month_from = filters.DateFilter(method="filter_month_from")
    month_to = filters.DateFilter(method="filter_month_to")

    def filter_month(self, queryset, name, value):
        return queryset.filter(month=normalize_month(value))

    def filter_month_from(self, queryset, name, value):
        return queryset.filter(month__gte=normalize_month(value))

    def filter_month_to(self, queryset, name, value):
        return queryset.filter(month__lte=normalize_month(value))

    class Meta:
        model = Budget
        fields = ["month", "month_from", "month_to", "category"]
