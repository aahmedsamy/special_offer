# Generated by Django 2.2 on 2019-07-05 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_advertisernotification_refuesed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisernotification',
            old_name='refuesed',
            new_name='refused',
        ),
    ]
