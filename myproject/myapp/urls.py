from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('predict/', views.prediction, name='predictions'),
    path('predict/', views.admin_dashboard, name='admin_dashboard'),

    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/update/<int:pk>/', views.role_update, name='role_update'),
    path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)