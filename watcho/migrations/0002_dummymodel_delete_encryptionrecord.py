# Generated by Django 4.2.19 on 2025-03-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcho', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='EncryptionRecord',
        ),
    ]
