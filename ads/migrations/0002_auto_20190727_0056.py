# Generated by Django 2.2 on 2019-07-26 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('ads', '0001_initial'),
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='advertiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Publisher', verbose_name='Advertiser'),
        ),
        migrations.AddField(
            model_name='ad',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.Discount', verbose_name='Discount'),
        ),
        migrations.AddField(
            model_name='ad',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.Offer', verbose_name='Offer'),
        ),
    ]