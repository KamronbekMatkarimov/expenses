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
        if getattr(category, "user_id", None) != request.user.id:
            raise serializers.ValidationError("Нельзя использовать чужую категорию")
        return category

    def validate_month(self, value):
        return normalize_month(value)

    def validate(self, attrs):
        request = self.context["request"]

        month = attrs.get("month", getattr(self.instance, "month", None))
        category = attrs.get("category", getattr(self.instance, "category", None))

        if month:
            month = normalize_month(month)
            attrs["month"] = month

        if month and category:
            qs = Budget.objects.filter(user=request.user, category=category, month=month)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({
                    "non_field_errors": [
                        "Бюджет на эту категорию и месяц уже существует. Используй PATCH/PUT."
                    ]
                })

        return attrs
