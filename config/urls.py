from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin already exists")

    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="Admin12345!"
    )
    return HttpResponse("Admin created successfully")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("create-admin/", create_admin),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/users/", include("users.urls")),
    path("api/expenses/", include("expenses.urls")),
    path("api/budgets/", include("budgets.urls")),
    path("api/reports/", include("reports.urls")),
]