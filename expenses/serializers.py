from rest_framework import serializers
from .models import Expense, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "description",
            "date",
            "receipt",
            "category",
            "category_name",
        ]
        read_only_fields = ["id", "category_name"]

    def validate_category(self, category):
        request = self.context["request"]
        if request.user.is_staff:
            return category
        if category.user_id != request.user.id:
            raise serializers.ValidationError("Нельзя использовать чужую категорию")
        return category
