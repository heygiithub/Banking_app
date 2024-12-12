from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('deposit/',views.deposit, name='deposit'),
    path('withdraw/',views.withdraw, name='withdraw'),
    path('check_balance/',views.check_balance, name='check_balance'),
    path('logout/',views.logout, name='logout'),
]
