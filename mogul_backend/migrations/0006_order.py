# Generated by Django 3.1.7 on 2021-02-26 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mogul_backend', '0005_auto_20210226_0234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('duration', models.IntegerField()),
                ('is_buy_order', models.BooleanField(default=0)),
                ('is_corporation', models.BooleanField(default=0)),
                ('issued', models.DateTimeField()),
                ('location_id', models.BigIntegerField()),
                ('min_volume', models.IntegerField()),
                ('order_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('range', models.CharField(default='0', max_length=16)),
                ('region_id', models.IntegerField()),
                ('type_id', models.IntegerField()),
                ('volume_remain', models.IntegerField()),
                ('volume_total', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, help_text='The user to whom this transaction belongs.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]