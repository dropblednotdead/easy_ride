# Generated by Django 5.2.1 on 2025-05-14 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_ride', '0008_alter_sales_end_date_alter_sales_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='sale_percent',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Процент скидки'),
        ),
    ]
