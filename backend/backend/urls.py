"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenRefreshView
from appointments.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # NOTE: registration is handled via the appointments app API.
    # The following TemplateView was causing POSTs to /api/register/ to
    # return HTML instead of JSON, so it was removed.
    # path('api/register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('appointments.urls')),
    # simple health check endpoint used by front‑end to detect backend status
    path('api/health/', lambda request: JsonResponse({'status': 'ok'}), name='health'),
    # Redirect site root to frontend login page
    path('', lambda request: redirect('/login/'), name='root'),
]
