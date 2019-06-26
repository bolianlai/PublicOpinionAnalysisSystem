from django.contrib import admin
from . import models

# Register your models here.

# Custom Action

# Push Site to Redis
# def make_push_redis(modeladmin, request, queryset):
#     result = queryset.all()
#     print(result)
#     for r in result:
        
#         r.site_url
#     modeladmin.message_user(request, '提交成功')
# make_push_redis.short_description = "提交所选的 采集站点列表"


# @admin.register(models.CrawlList)
# class CrawlListAdmin(admin.ModelAdmin):
#     list_display = ('site_name', 'spider_name', 'redis_key', 'seconds', 'datetime', 'start_api')
#     search_fields = ['site_name', 'spider_name']
#     list_filter = ['spider_name', 'datetime']
