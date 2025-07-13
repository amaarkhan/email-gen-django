from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('send/', views.send_email, name='send_email'),
    path('scheduled/', views.ScheduledEmailsView.as_view(), name='scheduled_emails'),
    path('cancel/<int:pk>/', views.cancel_email, name='cancel_email'),
    path('debug/scheduler/', views.debug_scheduler, name='debug_scheduler'),
    path('test_scheduler/', views.test_scheduler, name='test_scheduler'),
]
