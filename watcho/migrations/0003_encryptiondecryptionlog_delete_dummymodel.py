# Generated by Django 4.2.19 on 2025-03-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcho', '0002_dummymodel_delete_encryptionrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptionDecryptionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plain_text', models.TextField(blank=True, null=True)),
                ('encrypted_text', models.TextField(blank=True, null=True)),
                ('decrypted_text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DummyModel',
        ),
    ]
