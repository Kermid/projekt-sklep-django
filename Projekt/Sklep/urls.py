from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='Panel_glowny'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]