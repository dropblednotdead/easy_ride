# Generated by Django 5.2.1 on 2025-05-14 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_ride', '0006_userinformation_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название'),
        ),
    ]
