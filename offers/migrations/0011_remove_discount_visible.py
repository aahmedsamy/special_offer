# Generated by Django 2.2 on 2019-04-26 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0010_auto_20190426_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='visible',
        ),
    ]