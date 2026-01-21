from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'category_name', 'month', 'amount']