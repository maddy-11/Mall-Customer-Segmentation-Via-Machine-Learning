# Generated by Django 4.1.4 on 2023-02-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0008_vouchers_category_alter_vouchers_voucher'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster', models.IntegerField()),
                ('p_name', models.CharField(max_length=100)),
            ],
        ),
    ]