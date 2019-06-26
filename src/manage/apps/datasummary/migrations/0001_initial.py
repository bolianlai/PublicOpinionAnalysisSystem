# Generated by Django 2.2.1 on 2019-06-03 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('intro', models.CharField(max_length=200, verbose_name='摘要')),
                ('content_url', models.CharField(max_length=200, verbose_name='链接')),
                ('content_from', models.CharField(max_length=20, verbose_name='来源')),
                ('media_type', models.CharField(max_length=10, verbose_name='媒体类型')),
                ('lyric_attribute', models.CharField(choices=[(1, '正面'), (0, '中立'), (-1, '反面')], max_length=1, verbose_name='舆情属性')),
                ('publish_time', models.DateTimeField(verbose_name='发表时间')),
                ('update_time', models.DateTimeField(verbose_name='采集时间')),
                ('correlation', models.FloatField(verbose_name='关联度')),
            ],
            options={
                'verbose_name': '数据汇总',
                'verbose_name_plural': '数据汇总',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100, verbose_name='部门名称')),
                ('notice_email', models.EmailField(max_length=254, verbose_name='通知邮箱')),
                ('register_time', models.DateTimeField(verbose_name='注册时间')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='联系地址')),
                ('contract', models.TextField(blank=True, verbose_name='部门备注')),
            ],
            options={
                'verbose_name': '部门管理',
                'verbose_name_plural': '部门管理',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=100, verbose_name='组织名称')),
                ('contract', models.TextField(blank=True, verbose_name='组织备注')),
            ],
            options={
                'verbose_name': '组织名称',
                'verbose_name_plural': '组织名称',
            },
        ),
        migrations.CreateModel(
            name='ReportEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='上报标题')),
                ('content', models.TextField(verbose_name='上报内容')),
                ('report_time', models.DateTimeField(verbose_name='上报时间')),
                ('address', models.CharField(max_length=100, verbose_name='事件地点')),
                ('contract', models.CharField(max_length=100, verbose_name='联系方式')),
                ('deal_with', models.BooleanField(default=False, verbose_name='是否已处理')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportevents', to=settings.AUTH_USER_MODEL, verbose_name='处理人员')),
            ],
            options={
                'verbose_name': '上报舆情',
                'verbose_name_plural': '上报舆情',
            },
        ),
        migrations.CreateModel(
            name='PublicNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('intro', models.CharField(max_length=200, verbose_name='摘要')),
                ('report_time', models.DateTimeField(verbose_name='通知时间')),
                ('address', models.CharField(max_length=100, verbose_name='通知部门')),
                ('contract', models.CharField(max_length=100, verbose_name='联系方式')),
                ('deal_with', models.BooleanField(default=False, verbose_name='是否已处理')),
                ('deal_with_time', models.DateTimeField(verbose_name='处理时间')),
                ('department', models.ManyToManyField(blank=True, related_name='publicnotices', to='datasummary.Department', verbose_name='处理部门')),
            ],
            options={
                'verbose_name': '舆情通知',
                'verbose_name_plural': '舆情通知',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='department_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='datasummary.Organization', verbose_name='部门归属'),
        ),
    ]
