# Generated by Django 2.2 on 2019-05-09 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20190509_0451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='publisher',
            name='phone',
            field=models.CharField(default=1, max_length=20, verbose_name='Phone'),
            preserve_default=False,
        ),
    ]
