# Generated by Django 2.0.1 on 2018-02-25 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DimeCoins', '0016_dollar_dollar_dollar'),
    ]

    operations = [
        migrations.CreateModel(
            name='B_AT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.BigIntegerField(default=0, verbose_name='Date of Price')),
                ('open', models.FloatField(default=0.0)),
                ('close', models.FloatField(default=0.0)),
                ('high', models.FloatField(default=0.0)),
                ('low', models.FloatField(default=0.0)),
                ('total_supply', models.FloatField(default=0.0)),
                ('volume', models.FloatField(default=0.0)),
                ('market_cap', models.FloatField(default=0.0)),
                ('currency', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='DimeCoins.Currency')),
                ('xchange', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='DimeCoins.Xchange')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
