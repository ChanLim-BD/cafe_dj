# Generated by Django 3.2.18 on 2023-04-29 01:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=45),
        ),
    ]
