# Generated by Django 2.2 on 2019-07-02 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0026_remove_discount_price'),
        ('users', '0017_delete_subscriptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_subscription', to='offers.Discount', verbose_name='Discount')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_subscription', to='offers.Offer', verbose_name='Offer')),
                ('searcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searcher_subscription', to='users.Searcher', verbose_name='Searcher')),
            ],
        ),
    ]