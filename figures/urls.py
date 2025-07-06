from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_id>/create_figure/', views.create_figure, name='create_figure'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('package/<int:package_id>/buy/', views.buy_package, name='buy_package'),
    path('figure/<int:user_figure_id>/sell/', views.set_figure_for_sale, name='set_figure_for_sale'),
    path('figure/<int:user_figure_id>/transfer/', views.transfer_figure, name='transfer_figure'),
    path('event/<int:event_id>/create_package/', views.create_package, name='create_package'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('figure/<int:user_figure_id>/buy/', views.buy_figure, name='buy_figure'),
]
