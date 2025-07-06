from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/buy_ticket/', views.buy_ticket, name='buy_ticket'),
]
