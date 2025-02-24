from django.db import models


class ProcessedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    is_processed = models.BooleanField(default=False)
    is_processing = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='pending')
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    additional_info = models.TextField(blank=True, null=True)
    delivery_type = models.CharField(max_length=50)
    price = models.FloatField()
    book_language = models.CharField(max_length=255, default='Українська')
    payment_status = models.CharField(max_length=50, default='pending')  # Добавляем поле статуса
    language = models.CharField(max_length=10, default='ua')  # Добавляем поле языка
    created_at = models.DateTimeField(auto_now_add=True)