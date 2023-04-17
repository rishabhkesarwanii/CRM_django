from django.contrib import admin
from django.urls import path, include
from leads.views import LandingPageView, SignUpView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('admin/', admin.site.urls), # 1
    path('', LandingPageView.as_view(), name="landing-page"), # 2

    path('leads/', include('leads.urls', namespace="leads")), # 3
    path('agents/', include('agents.urls', namespace="agents")),
    
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('login/', LoginView.as_view(), name='login'), # 5
    path('logout/', LogoutView.as_view(), name='logout'), # 6
    path('signup/', SignUpView.as_view(), name='signup'), # 4
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
