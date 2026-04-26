from django.urls import path
from django.conf import settings          # <--- THIS IS THE FIX
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.components_list, name='components_list'),
    path('component/<int:pk>/', views.component_detail, name='component_detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)