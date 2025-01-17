# Generated by Django 2.2 on 2019-06-28 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0024_auto_20190629_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_discount', to='offers.Discount', verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='like',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_offer', to='offers.Offer', verbose_name='Offer'),
        ),
    ]
