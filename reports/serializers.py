from rest_framework import serializers
from budgets.models import normalize_month


class ReportQuerySerializer(serializers.Serializer):
    month = serializers.DateField(required=True)

    def validate_month(self, value):
        return normalize_month(value)


class ReportEmailRequestSerializer(serializers.Serializer):
    month = serializers.DateField(required=True)
    to_email = serializers.EmailField(required=True)

    def validate_month(self, value):
        return normalize_month(value)


class MonthlyReportResponseSerializer(serializers.Serializer):
    month = serializers.DateField()
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    budget_delta = serializers.DecimalField(max_digits=12, decimal_places=2)
    by_category = serializers.ListField(child=serializers.DictField())
    over_budget = serializers.ListField(child=serializers.DictField())
