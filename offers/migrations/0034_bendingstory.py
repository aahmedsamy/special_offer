# Generated by Django 2.2 on 2019-07-20 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0033_auto_20190720_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='BendingStory',
            fields=[
            ],
            options={
                'verbose_name': 'Bending Story',
                'verbose_name_plural': 'Bending Stories',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('offers.story',),
        ),
    ]
