import django_filters
from datetime import datetime
from .models import Budget, normalize_month


class BudgetFilter(django_filters.FilterSet):

    month = django_filters.CharFilter(method="filter_month")
    category = django_filters.NumberFilter(field_name="category_id")

    class Meta:
        model = Budget
        fields = ["category", "month"]

    def filter_month(self, queryset, name, value):
        value = (value or "").strip()
        if not value:
            return queryset

        try:
            dt = datetime.strptime(value, "%Y-%m")
            month_date = normalize_month(dt.date())
            return queryset.filter(month=month_date)
        except ValueError:
            pass

        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            month_date = normalize_month(dt.date())
            return queryset.filter(month=month_date)
        except ValueError:
            return queryset.none()
