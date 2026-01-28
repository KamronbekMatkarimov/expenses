from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from expenses.models import Category


def normalize_month(value):
    return value.replace(day=1)


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    month = models.DateField(help_text="Month stored as first day (YYYY-MM-01)")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "month"],
                name="uniq_budget_user_category_month",
            )
        ]

    def clean(self):
        if self.month and self.month.day != 1:
            raise ValidationError({"month": "month must be first day of month (YYYY-MM-01)."})

    def save(self, *args, **kwargs):
        if self.month:
            self.month = normalize_month(self.month)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.month.strftime('%Y-%m')})"
