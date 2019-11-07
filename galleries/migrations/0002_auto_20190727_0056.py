# Generated by Django 2.2 on 2019-07-26 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offers', '0001_initial'),
        ('galleries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plusitemimage',
            name='plus_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plus_item_image', to='offers.PlusItem'),
        ),
        migrations.AddField(
            model_name='offerimage',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_images', to='offers.Offer'),
        ),
        migrations.AddField(
            model_name='discountimage',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_images', to='offers.Discount'),
        ),
    ]
