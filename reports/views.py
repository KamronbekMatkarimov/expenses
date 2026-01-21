from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from expenses.models import Expense
from budgets.models import Budget
from datetime import datetime
from django.http import HttpResponse
import csv
from django.core.mail import EmailMessage
from io import StringIO

class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month_str = request.query_params.get('month')
        export = request.query_params.get('export')

        if not month_str:
            return Response({"error": "month параметр обязателен (YYYY-MM)"}, status=400)

        try:
            month_date = datetime.strptime(month_str, "%Y-%m")
        except ValueError:
            return Response({"error": "Неверный формат месяца"}, status=400)

        expenses = Expense.objects.filter(
            user=request.user,
            date__year=month_date.year,
            date__month=month_date.month
        )

        budgets = Budget.objects.filter(
            user=request.user,
            month__year=month_date.year,
            month__month=month_date.month
        )

        category_expenses = {}
        for e in expenses:
            name = e.category.name
            category_expenses[name] = category_expenses.get(name, 0) + float(e.amount)

        budget_limits = {b.category.name: float(b.amount) for b in budgets}

        budget_report = {}
        for category, spent in category_expenses.items():
            limit = budget_limits.get(category, 0)
            budget_report[category] = {
                "limit": limit,
                "spent": spent,
                "remaining": limit - spent,
                "over_budget": spent > limit if limit else False
            }

        total = float(expenses.aggregate(total=Sum('amount'))['total'] or 0)

        if export == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'
            writer = csv.writer(response)

            writer.writerow(['Category', 'Spent', 'Budget', 'Remaining', 'Over'])
            for k, v in budget_report.items():
                writer.writerow([k, v['spent'], v['limit'], v['remaining'], v['over_budget']])
            writer.writerow([])
            writer.writerow(['Total', total])
            return response

        return Response({
            "total_expenses": total,
            "category_expenses": category_expenses,
            "budget": budget_report
        })