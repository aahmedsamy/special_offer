# Generated by Django 2.2 on 2019-08-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='address',
            field=models.CharField(max_length=250, null=True, verbose_name='Address'),
        ),
    ]
