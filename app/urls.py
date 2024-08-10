from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-user/', views.create_user, name='create-user'),
    path('create-category/', views.create_category, name='create-category'),
    path('create-loan/', views.create_loan, name='create-loan'),
    path('add-refund/', views.add_refund, name='add-refund'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.update_profile, name='update-profile'),
]
