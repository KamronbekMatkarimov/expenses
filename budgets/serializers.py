from rest_framework import serializers
from .models import Budget, normalize_month


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Budget
        fields = ["id", "category", "category_name", "month", "amount"]
        read_only_fields = ["id", "category_name"]

    def validate_category(self, category):
        request = self.context["request"]
        if request.user.is_staff:
            return category
        if category.user_id != request.user.id:
            raise serializers.ValidationError("Нельзя использовать чужую категорию")
        return category

    def validate_month(self, value):
        return normalize_month(value)
