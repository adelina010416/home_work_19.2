# Generated by Django 4.2.4 on 2023-11-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_verified_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified_password',
            field=models.CharField(blank=True, null=True, verbose_name='ключ для верификации'),
        ),
    ]
