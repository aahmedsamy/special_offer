# Generated by Django 2.2 on 2019-04-26 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0008_auto_20190426_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='visible',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='visible',
        ),
    ]
