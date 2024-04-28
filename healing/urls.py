from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('doctors/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('', lambda request: redirect("/authentication/login/")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)