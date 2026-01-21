from rest_framework import serializers
from .models import Expense, Category

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['id', 'name', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.CharField(source='category.name', read_only=True)

    def validate_category(self, category):
        if category.user != self.context['request'].user:
            raise serializers.ValidationError("Нельзя использовать чужую категорию")
        return category

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'description', 'date',
            'receipt', 'user', 'category', 'category_name'
        ]