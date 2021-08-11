# Generated by Django 3.2.6 on 2021-08-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_design'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='design',
            name='cart_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='cart id'),
        ),
        migrations.AlterField(
            model_name='design',
            name='cart_line',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
