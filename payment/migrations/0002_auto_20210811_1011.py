# Generated by Django 3.2.6 on 2021-08-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'PAYMENT'), (2, 'REFUND'), (3, 'PARTIAL REFUND')], default=1),
        ),
        migrations.AlterField(
            model_name='payment',
            name='rzp_order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='razorpay order id'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Created', 'CREATED'), ('Authorized', 'AUTHORIZED'), ('Captured', 'CAPTURED'), ('Refunded', 'REFUNDED'), ('PartiallyRefund', 'PARTIALLY REFUNDED'), ('Failed', 'FAILED')], default='Created', max_length=50),
        ),
    ]
