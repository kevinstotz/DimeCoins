# Generated by Django 2.0.1 on 2018-02-25 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DimeCoins', '0021_acci_babcoin_bils_bod_bre_c0c0_caid_capt_cbit_clt_cry_dcyp_debune_eb3c_emirg_eruns_floz_fry_gss_gtfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jack',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='jack',
            name='xchange',
        ),
        migrations.DeleteModel(
            name='JACK',
        ),
    ]