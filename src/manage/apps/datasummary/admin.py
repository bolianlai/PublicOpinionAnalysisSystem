from django.contrib import admin
from . import models



from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse

# 发送单个邮件，指的是发送单个邮件 可调用
def to_send_email(topic, content, url, receive_list):
    from_who = settings.EMAIL_FROM
    subject = '{}-{}-舆情预警!'.format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), topic)  # 发送的主题
    meg_html = '<p>{}</p><a href="{}">点击跳转</a>'.format(content, url)
    send_mail(subject, message=content, from_email=from_who, recipient_list=receive_list, html_message=meg_html)
    return True

# 发送多个邮件,指的是多封不同的邮件  
def to_send_mass_email(topic, message, url, receive_list):
    from_who = settings.EMAIL_FROM
    subject = '{}-{}-舆情预警!'.format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), topic)  # 发送的主题
    meg_html = '<p>{}</p><a href="{}">点击跳转</a>'.format(message, url)
    message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
    message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
    send_mass_mail((message1, message2), fail_silently=False)
    return True


# Custom Action

# Push Site to Redis
def reporting_grievances(modeladmin, request, queryset):
    result = queryset.all()
    # print(result)
    for r in result:
        # d = models.DataSummary.objects.get(id=r.id) 
        # print(r.summary.all())
        receive_list = [s.notice_email for s in r.summary.all()]
        # print(receive_list)
        to_send_email(r.id, r.intro, r.content_url, receive_list)
    modeladmin.message_user(request, '提交成功')
reporting_grievances.short_description = "上报舆情到相关部门"




@admin.register(models.DataSummary)
class DataSummaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'content_url','content_from','media_type', 'lyric_attribute', 'publish_time', 'update_time', 'correlation')
    search_fields = ('title', 'intro','content_from','media_type', 'lyric_attribute')
    list_filter = ('content_from','media_type', 'lyric_attribute', 'publish_time', 'update_time', 'correlation')
    actions = [reporting_grievances]

@admin.register(models.ReportEvent)
class ReportEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_time', 'address','contract','deal_with', 'user')
    search_fields = ('title','address','user.username')
    list_filter = ('report_time','deal_with')
    # list_editable = ['deal_with',]
    actions = [reporting_grievances]


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_owner', 'notice_email','register_time','contract', 'address', 'remark')
    search_fields = ('department_name','department_owner','notice_email','remark')
    list_filter = ('department_owner','register_time')


@admin.register(models.PublicNotice)
class PublicNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'report_time','deal_with', 'deal_with_time')
    search_fields = ('title','intro','remark')
    list_filter = ('report_time','deal_with', 'deal_with_time')


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'remark')
    search_fields = ('organization_name','remark')


@admin.register(models.EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'report_time', 'remark')
    search_fields = ('title','remark')


@admin.register(models.CommentContent)
class CommentContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'commentary','update_time',  'remark')
    search_fields = ('title','commentary',  'remark')

    def save_model(self, request, obj, form, change):
        from snownlp import SnowNLP

        s = SnowNLP(obj.comment)
        # keywords = s.keywords(3)
        obj.commentary =  s.keywords(3)
        super().save_model(request, obj, form, change)
