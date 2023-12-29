from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('admin_adminlte.urls'),),
    path("api/v1/user/", include("user_app.urls")),
]
