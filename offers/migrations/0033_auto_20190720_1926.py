# Generated by Django 2.2 on 2019-07-20 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20190712_1108'),
        ('offers', '0032_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Publisher', verbose_name='Publisher'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('Bending', 'Bending'), ('Declined', 'Declined'), ('Approved', 'Approved')], default='Bending', max_length=50, verbose_name='Status'),
        ),
    ]
