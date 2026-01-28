from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib.auth import get_user_model


def create_admin(request):
    User = get_user_model()

    username = "admin"
    password = "admin12345"
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        return HttpResponse("✅ Superuser created: admin / admin12345")

    return HttpResponse("ℹ️ Superuser already exists")


def healthz(request):
    return HttpResponse("ok")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("create-admin/", create_admin),
    path("healthz/", healthz),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/users/", include("users.urls")),
    path("api/expenses/", include("expenses.urls")),
    path("api/budgets/", include("budgets.urls")),
    path("api/reports/", include("reports.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
