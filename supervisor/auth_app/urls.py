from django.urls import path
from . import views
#password reset option..!
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('dashboard',views.dashboard_view,name='dashboard'),
    # 1. Submit password reset Form..
    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name='auth/PassRestForm.html'),
         name='reset_password'),
    # 2. Email sent Successful msg..!
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # 
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confrim'),
    # password successfuly changed msg.!
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]