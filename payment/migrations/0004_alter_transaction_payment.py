# Generated by Django 3.2.6 on 2021-08-11 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='payment.payment'),
        ),
    ]
