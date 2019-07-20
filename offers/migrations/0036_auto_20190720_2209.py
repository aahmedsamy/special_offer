# Generated by Django 2.2 on 2019-07-20 18:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0035_auto_20190720_2032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-id'], 'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.AddField(
            model_name='story',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='story',
            name='advertiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertiser_stories', to='users.Publisher', verbose_name='Advertiser'),
        ),
    ]