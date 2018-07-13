# Generated by Django 2.0.6 on 2018-07-13 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('purchases', '0005_auto_20180713_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='customer',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='customers.Customer'),
            preserve_default=False,
        ),
    ]
