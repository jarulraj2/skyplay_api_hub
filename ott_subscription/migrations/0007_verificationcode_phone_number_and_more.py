# Generated by Django 4.2.19 on 2025-03-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ott_subscription', '0006_verificationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationcode',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
