# Generated by Django 2.2 on 2019-05-13 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0012_auto_20190426_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='end_date',
            field=models.DateField(verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='start_date',
            field=models.DateField(verbose_name='Start date'),
        ),
    ]
