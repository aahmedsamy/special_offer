# Generated by Django 2.2 on 2019-07-05 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20190705_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisernotification',
            name='refused',
        ),
        migrations.AddField(
            model_name='advertisernotification',
            name='status',
            field=models.CharField(default=1, max_length=50, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchernotification',
            name='status',
            field=models.CharField(default=1, max_length=50, verbose_name='Status'),
            preserve_default=False,
        ),
    ]
