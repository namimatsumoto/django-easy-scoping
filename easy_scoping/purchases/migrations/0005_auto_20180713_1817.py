# Generated by Django 2.0.6 on 2018-07-13 18:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_auto_20180711_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='sale_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
