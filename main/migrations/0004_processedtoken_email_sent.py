# Generated by Django 5.1.5 on 2025-02-08 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_processedtoken_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='processedtoken',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
