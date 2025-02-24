from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('en/', views.index_en, name='index_en'),
    path('submit-ukraine/', views.submit_ukraine_form, name='submit_ukraine_form'),
    path('submit-world/', views.submit_world_form, name='submit_world_form'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('pay-callback/', views.pay_callback, name='pay_callback'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('check_payment_status', views.check_payment_status, name='check_payment_status'),
    path('payment/success/ua/', views.payment_success_ua, name='payment_success_ua'),
    path('en/payment/success/', views.payment_success_en, name='payment_success_en'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment/cancel/uk/', views.payment_cancel_ua, name='payment_cancel_ua'),
    path('payment/cancel/en', views.payment_cancel_en, name='payment_cancel_en'),
]
