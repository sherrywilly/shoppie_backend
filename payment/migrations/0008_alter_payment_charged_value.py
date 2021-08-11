# Generated by Django 3.2.6 on 2021-08-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_payment_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='charged_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
