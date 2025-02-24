# Generated by Django 5.1.5 on 2025-02-09 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_processedtoken_is_processing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('delivery_type', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('book_language', models.CharField(default='Українська', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
