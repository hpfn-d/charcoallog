# Generated by Django 2.2.4 on 2019-08-20 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0019_auto_20181118_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newinvestmentdetails',
            name='quant',
            field=models.IntegerField(),
        ),
    ]
