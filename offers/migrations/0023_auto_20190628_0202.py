# Generated by Django 2.2 on 2019-06-27 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20190510_1747'),
        ('offers', '0022_category_small_image_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='advertiser',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('advertiser', 'offer', 'discount')},
        ),
    ]