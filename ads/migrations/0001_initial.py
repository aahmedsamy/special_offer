# Generated by Django 2.2 on 2019-07-26 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('image', models.ImageField(upload_to='ads/images', verbose_name='Ad Image')),
                ('position', models.CharField(choices=[('Top', 'Top'), ('Buttom', 'Buttom')], max_length=256, verbose_name='Position')),
                ('period', models.PositiveSmallIntegerField(help_text='Please set ad period in seconds.', verbose_name='Period')),
                ('start_date', models.DateField(help_text='Start viewing date', verbose_name='Start date')),
                ('end_date', models.DateField(help_text='End viewing date', verbose_name='End date')),
            ],
            options={
                'verbose_name': 'Ad',
                'verbose_name_plural': 'Ads',
            },
        ),
    ]
