# Generated by Django 3.2.6 on 2021-08-12 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_total_order_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_charges',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_order_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
