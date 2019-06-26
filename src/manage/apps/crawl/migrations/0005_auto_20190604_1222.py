# Generated by Django 2.2.1 on 2019-06-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0004_auto_20190604_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crawllist',
            options={'verbose_name': '采集站点', 'verbose_name_plural': '采集站点'},
        ),
        migrations.AddField(
            model_name='crawllist',
            name='status',
            field=models.CharField(blank=True, choices=[('1', '存活'), ('0', '宕机')], max_length=2, null=True, verbose_name='节点状态'),
        ),
        migrations.AlterField(
            model_name='crawllist',
            name='remark',
            field=models.CharField(max_length=20, verbose_name='备注'),
        ),
    ]
