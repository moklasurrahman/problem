"""booking_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page2, name='home_page'),
    path('taj', views.taj, name='taj_page'),
    # path('home2', views.home_page2, name='home_page2'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('my-account/', views.my_account, name='my_account'),

    path('u-profile/', views.user_profile, name='user_profile'),



    path('guest-login/', views.guest_login, name="guest_login"),
    path('contact-us/', views.contact_page, name='contact_page'),
    path('about-us/', views.about_us, name='about_us'),
    path('terms/', views.terms, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
    path('payment-policy/', views.payment_policy, name="payment_policy"),
    path('cookie-policy/', views.cookie_policy, name="cookie_policy"),
    path('fqa/', views.fqa_page, name="fqa_page"),
    path('update-profile/', views.change_profile, name="update_profile"),
    path('change-password', views.change_password, name="change_password"),
    path('phone-verification/', views.verify_phone_code, name="verify_phone_code"),
    path('login-phone-ajax/', views.phone_code_ajax, name="phone_code_ajax"),
    path('phone-verification-ajax/', views.verify_phone_code_ajax, name="verify_phone_code_ajax"),
    path('verify-phone-code-error-ajax/', views.verify_phone_code_error_ajax, name="verify_phone_code_error_ajax"),
    path('phone-verification-error/', views.verify_phone_code_error, name="verify_phone_code_error"),
    path('air/', include('air.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
      path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns