# Generated by Django 3.2.6 on 2022-02-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0049_auto_20211229_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='is_iot_core',
            field=models.BooleanField(default=False, verbose_name='IOT core'),
        ),
    ]
