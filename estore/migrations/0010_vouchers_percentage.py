# Generated by Django 4.1.4 on 2023-02-11 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0009_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='vouchers',
            name='percentage',
            field=models.IntegerField(null=True),
        ),
    ]
