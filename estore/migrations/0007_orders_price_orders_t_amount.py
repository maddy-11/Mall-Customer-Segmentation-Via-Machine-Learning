# Generated by Django 4.1.4 on 2023-02-09 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0006_rename_rattigns_review_rattings'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='t_amount',
            field=models.IntegerField(null=True),
        ),
    ]
