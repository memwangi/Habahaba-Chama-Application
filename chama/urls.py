from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homepage, name='home'),
    # path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('register/', views.signup, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

]
