# Generated by Django 5.0 on 2023-12-28 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer_app', '0003_alter_buyer_user_id'),
        ('user_app', '0002_remove_userprofile_buyer_remove_userprofile_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_app.userprofile'),
        ),
    ]
