from django.urls import path
from login.views import register, basic, profile, logout1
from musicapp import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', basic, name="basic"),
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),
    path('logout/', logout1, name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='login/password_reset.html'), name="reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='login/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='login/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='login/password_reset_complete.html'), name="password_reset_complete"),
    path('profile/', profile, name='profile'),
    
]


if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,
                          #document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
