# Generated by Django 3.2.6 on 2021-08-11 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotp',
            name='otp',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
