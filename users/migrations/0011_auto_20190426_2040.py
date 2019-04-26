# Generated by Django 2.2 on 2019-04-26 16:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_searcher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='work_end_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Work ends at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publisher',
            name='work_start_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Work starts at'),
            preserve_default=False,
        ),
    ]
