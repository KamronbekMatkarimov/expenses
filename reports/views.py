from datetime import datetime
from io import StringIO
import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers

from expenses.models import Expense
from budgets.models import Budget


class ReportEmailSerializer(serializers.Serializer):
    month = serializers.RegexField(
        regex=r"^\d{4}-\d{2}$",
        error_messages={"invalid": "month must be in YYYY-MM format"},
    )
    to_email = serializers.EmailField()


def parse_month_or_400(month_str: str):
    try:
        return datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        return None


def build_report(user, year: int, month: int):
    expenses_qs = (
        Expense.objects.filter(user=user, date__year=year, date__month=month)
        .select_related("category")
    )

    grouped = expenses_qs.values("category__name").annotate(spent=Sum("amount")).order_by()

    total = expenses_qs.aggregate(total=Sum("amount"))["total"] or 0

    budgets_qs = Budget.objects.filter(user=user, month__year=year, month__month=month).select_related("category")
    budget_limits = {b.category.name: b.amount for b in budgets_qs}

    category_expenses = {}
    chart_data = []
    budget_report = {}
    over_budget_categories = []

    for row in grouped:
        name = row["category__name"]
        spent = row["spent"] or 0
        category_expenses[name] = float(spent)

        percent = float(spent) / float(total) * 100 if total else 0.0
        chart_data.append({"category": name, "spent": float(spent), "percent": round(percent, 2)})

        limit = budget_limits.get(name, 0)
        remaining = (limit - spent) if limit else 0
        over_budget = bool(limit and spent > limit)

        if over_budget:
            over_budget_categories.append(name)

        budget_report[name] = {
            "limit": float(limit) if limit else 0.0,
            "spent": float(spent),
            "remaining": float(remaining) if limit else 0.0,
            "over_budget": over_budget,
        }

    return {
        "total_expenses": float(total),
        "category_expenses": category_expenses,
        "chart_data": chart_data,
        "budget": budget_report,
        "over_budget_categories": over_budget_categories,
    }


def report_to_csv_text(report: dict):
    buf = StringIO()
    writer = csv.writer(buf)

    writer.writerow(["Category", "Spent", "Budget", "Remaining", "Over", "Percent"])
    for category, b in report["budget"].items():
        percent = 0.0
        for item in report["chart_data"]:
            if item["category"] == category:
                percent = item["percent"]
                break
        writer.writerow([category, b["spent"], b["limit"], b["remaining"], b["over_budget"], percent])

    writer.writerow([])
    writer.writerow(["Total", report["total_expenses"]])
    return buf.getvalue()


class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month_str = request.query_params.get("month")
        export = request.query_params.get("export")

        if not month_str:
            return Response(
                {"error": {"code": 400, "message": "month param is required (YYYY-MM)", "details": None}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        month_dt = parse_month_or_400(month_str)
        if not month_dt:
            return Response(
                {"error": {"code": 400, "message": "Invalid month format, use YYYY-MM", "details": None}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = build_report(request.user, month_dt.year, month_dt.month)

        if export == "csv":
            csv_text = report_to_csv_text(report)
            response = HttpResponse(csv_text, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="report.csv"'
            return response

        return Response(report)


class MonthlyReportEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        month_str = serializer.validated_data["month"]
        to_email = serializer.validated_data["to_email"]

        month_dt = parse_month_or_400(month_str)
        if not month_dt:
            return Response(
                {"error": {"code": 400, "message": "Invalid month format, use YYYY-MM", "details": None}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = build_report(request.user, month_dt.year, month_dt.month)
        csv_text = report_to_csv_text(report)

        subject = f"Monthly Expense Report {month_str}"
        body = "Report is attached as CSV."

        email = EmailMessage(subject=subject, body=body, to=[to_email])
        email.attach(filename=f"report_{month_str}.csv", content=csv_text, mimetype="text/csv")
        email.send(fail_silently=False)

        return Response(
            {"message": "Hisobot email orqali yuborildi", "to": to_email, "month": month_str},
            status=status.HTTP_200_OK,
        )
