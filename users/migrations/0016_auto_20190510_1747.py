# Generated by Django 2.2 on 2019-05-10 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20190510_1747'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Holiday',
        ),
        migrations.AlterField(
            model_name='publisher',
            name='holidays',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Holidays'),
        ),
    ]
