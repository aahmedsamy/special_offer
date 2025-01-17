# Generated by Django 2.2 on 2019-06-07 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0016_auto_20190605_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferAndDiscountFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Feature name')),
                ('desc', models.TextField(max_length=1024, verbose_name='Description')),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_features', to='offers.Offer', verbose_name='Discount')),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offer_features', to='offers.Offer', verbose_name='Offer')),
            ],
        ),
    ]
