# Generated by Django 4.1 on 2023-08-17 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_ipam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaddress',
            name='xunmi_info',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='寻觅回填信息'),
        ),
    ]