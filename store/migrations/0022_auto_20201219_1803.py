# Generated by Django 3.1.4 on 2020-12-19 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_customer_joined'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Country',
            new_name='country',
        ),
    ]
