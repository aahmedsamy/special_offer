# Generated by Django 2.2 on 2019-04-26 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='publisher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='users.Publisher'),
        ),
        migrations.AlterField(
            model_name='user',
            name='searcher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='searcher', to='users.Searcher'),
        ),
    ]
