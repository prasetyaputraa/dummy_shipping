# Generated by Django 3.2.7 on 2022-02-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20220221_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptwrite',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='receiptwrite',
            name='no',
            field=models.CharField(max_length=36),
        ),
    ]