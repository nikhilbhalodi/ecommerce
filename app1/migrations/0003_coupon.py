# Generated by Django 3.1.4 on 2021-02-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
    ]