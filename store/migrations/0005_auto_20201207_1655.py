# Generated by Django 3.1.4 on 2020-12-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20201207_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='store.Tag'),
        ),
    ]
