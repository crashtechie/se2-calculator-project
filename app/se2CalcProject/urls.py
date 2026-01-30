from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.views.generic import TemplateView


def health_check(_request):
    """Lightweight health endpoint used by Docker/Nginx checks."""
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('health/', health_check, name='health'),
    path('ores/', include('ores.urls', namespace='ores')),
    path('components/', include('components.urls', namespace='components')),
    path('blocks/', include('blocks.urls', namespace='blocks')),  # ENH-0000007
]
