# Generated by Django 3.2.18 on 2023-04-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_account_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_staff',
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]