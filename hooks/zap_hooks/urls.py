from django.urls import path
from .views import webhook_handler

urlpatterns = [
    path('hooks/catch/<int:user_id>/<str:zap_id>/', webhook_handler, name='webhook_handler'),
]
