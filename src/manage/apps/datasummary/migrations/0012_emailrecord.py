# Generated by Django 2.2.1 on 2019-06-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasummary', '0011_auto_20190604_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='舆情名称')),
                ('intro', models.CharField(max_length=200, verbose_name='舆情摘要')),
                ('report_time', models.DateTimeField(verbose_name='通知时间')),
                ('notices', models.TextField(verbose_name='通知部门')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '邮件记录',
                'verbose_name_plural': '邮件记录',
            },
        ),
    ]