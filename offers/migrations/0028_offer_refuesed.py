# Generated by Django 2.2 on 2019-07-05 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0027_auto_20190703_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='refuesed',
            field=models.BooleanField(default=False, verbose_name='Refused'),
        ),
    ]