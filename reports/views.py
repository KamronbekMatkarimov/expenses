from decimal import Decimal

from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter

from budgets.models import Budget, normalize_month
from expenses.models import Expense, Category

from .serializers import (
    ReportQuerySerializer,
    ReportEmailRequestSerializer,
    MonthlyReportResponseSerializer,
)


def _month_range(month_first_day):
    """
    month_first_day: datetime.date (YYYY-MM-01)
    return: (start_date, end_date_inclusive)
    """
    if month_first_day.month == 12:
        next_month = month_first_day.replace(year=month_first_day.year + 1, month=1, day=1)
    else:
        next_month = month_first_day.replace(month=month_first_day.month + 1, day=1)
    end_date = next_month.fromordinal(next_month.toordinal() - 1)
    return month_first_day, end_date


def _build_monthly_report(user, month_first_day):
    start_date, end_date = _month_range(month_first_day)

    expenses_qs = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
    budgets_qs = Budget.objects.filter(user=user, month=month_first_day)

    total_expenses = expenses_qs.aggregate(s=Sum("amount"))["s"] or Decimal("0.00")
    total_budget = budgets_qs.aggregate(s=Sum("amount"))["s"] or Decimal("0.00")
    budget_delta = total_budget - total_expenses 

    by_cat_rows = (
        expenses_qs.values("category", "category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    by_category = []
    for row in by_cat_rows:
        total = row["total"] or Decimal("0.00")
        percent = Decimal("0.00")
        if total_expenses > 0:
            percent = (total / total_expenses) * Decimal("100.0")
        by_category.append(
            {
                "category_id": row["category"],
                "category_name": row["category__name"],
                "total": str(total),
                "percent": str(percent.quantize(Decimal("0.01"))),
            }
        )

    over_budget = []
    budgets = budgets_qs.select_related("category")
    for b in budgets:
        spent = (
            expenses_qs.filter(category=b.category).aggregate(s=Sum("amount"))["s"]
            or Decimal("0.00")
        )
        if spent > b.amount:
            over_budget.append(
                {
                    "category_id": b.category_id,
                    "category_name": b.category.name,
                    "budget": str(b.amount),
                    "spent": str(spent),
                    "over": str(spent - b.amount),
                }
            )

    return {
        "month": month_first_day,
        "total_expenses": total_expenses,
        "total_budget": total_budget,
        "budget_delta": budget_delta,
        "by_category": by_category,
        "over_budget": over_budget,
    }


class ReportsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="month",
                description="Report month. Any date accepted; will be normalized to YYYY-MM-01",
                required=True,
                type=str,
            )
        ],
        responses={200: MonthlyReportResponseSerializer},
        tags=["Reports"],
    )
    def get(self, request):
        ser = ReportQuerySerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        month_first_day = normalize_month(ser.validated_data["month"])
        report = _build_monthly_report(request.user, month_first_day)
        return Response(report, status=status.HTTP_200_OK)


class ReportEmailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ReportEmailRequestSerializer,
        responses={200: MonthlyReportResponseSerializer},
        tags=["Reports"],
    )
    def post(self, request):
        ser = ReportEmailRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        month_first_day = ser.validated_data["month"]
        to_email = ser.validated_data["to_email"]

        report = _build_monthly_report(request.user, month_first_day)

        report["email"] = {"to": to_email, "status": "not_implemented_yet"}

        return Response(report, status=status.HTTP_200_OK)
