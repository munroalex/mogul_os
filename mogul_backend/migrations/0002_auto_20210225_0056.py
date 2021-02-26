# Generated by Django 3.1.7 on 2021-02-25 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogul_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='margin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='state',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='station_name',
            field=models.CharField(default='Unknown', max_length=32),
        ),
        migrations.AddField(
            model_name='transaction',
            name='stock_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type_name',
            field=models.CharField(default='Unknown', max_length=32),
        ),
    ]