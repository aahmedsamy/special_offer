# Generated by Django 2.2 on 2019-06-07 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0019_auto_20190607_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offeranddiscountfeature',
            name='discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_features', to='offers.Discount', verbose_name='Discount'),
        ),
    ]