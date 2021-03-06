# Generated by Django 3.2.7 on 2022-02-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_rename_to_receiptwrite__to'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptwrite',
            name='cost',
            field=models.PositiveIntegerField(default=8000),
        ),
        migrations.AlterField(
            model_name='receiptwrite',
            name='status',
            field=models.CharField(choices=[('REC-ORGN', 'Received at origin'), ('DPRT-ORGN', 'Departed from origin'), ('ARVD-DSTN', 'Arrived at destination'), ('REC-DSTN', 'Received at destination')], max_length=255),
        ),
    ]
