from django.urls import path
from . import views

from django.contrib.auth import views as auth_views



urlpatterns=[
    path('',views.index, name='index'),
    path('account/',views.account, name='account'),
    path('invest/',views.invest, name='invest'),
    path('withdraw/',views.withdraw, name='withdraw'),
    path('transactions/',views.transactions, name='transactions'),
    path('plans/',views.plans, name='plans'),

    path('how it works/',views.how, name='how'),
    path('terms of use/',views.terms, name='terms'),
    path('about/',views.about, name='about'),

    path('register/',views.register, name='register'),
    path('login/',views.loginuser, name='login'),
    path('update/',views.update_profile, name='update'),
    path('logout/',views.logoutuser, name='logout'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "gainisis/authentication/reset/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "gainisis/authentication/reset/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "gainisis/authentication/reset/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "gainisis/authentication/reset/password_reset_done.html"), name ='password_reset_complete')
]