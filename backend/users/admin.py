from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry

from users.models import UserProfile, AccessTimeOutLogs, OpLogs
# ModerateLog, Moderate


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'nick_name', 'mobile', 'get_login_status', 'email']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message', 'object_repr']
    list_filter = ('user', 'action_flag')
    search_fields = ['action_flag', 'user', 'change_message']


admin.site.register(LogEntry, LogEntryAdmin)


@admin.register(OpLogs)
class OpLogsAdmin(admin.ModelAdmin):
    list_display = ['re_url', 're_method', 'access_time', 're_ip', 'user_agent', 'rp_code', 're_content', 're_time',
                    're_user',
                    ]  # rp_content 响应参数内容太多不展示
    list_filter = ('re_url', 're_user')
    search_fields = ['re_url', 're_user', 'rp_code']


@admin.register(AccessTimeOutLogs)
class AccessTimeOutLogsAdmin(admin.ModelAdmin):
    list_display = ['re_url', 're_method', 'access_time', 're_ip', 'user_agent', 'rp_code', 're_content', 're_time',
                    're_user',
                    ]  # rp_content 响应参数内容太多不展示
    list_filter = ('re_url', 're_user')
    search_fields = ['re_url', 're_user', 'rp_code']


# @admin.register(Moderate)
# # admin.site.register(要写的表)  与  @admin.register(要写的表)  功能是一样的
# class ModerateAdmin(admin.ModelAdmin):
#     """
#         *MySQL数据库moderate表：id, 名字, 内容，是否通过, 是否已审核
#         'id', 'name', 'incident', 'status', 'check'
#     """
#     # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
#     list_display = ('name', 'incident', 'status',)
#     # list_per_page设置每页显示多少条记录，默认是10条
#     list_per_page = 10
#     # list_filter过滤指定的字段
#     list_filter = ('name',)
#
#     # 修改admin页面actions的信息
#     actions = ['mak_pub', 'mak_pub1']
#
#     # 判断通过的
#     def mak_pub(self, request, queryset):
#         # 获取当前用户的名字
#         us = request.user
#         # 打印通过的数据
#         for i in queryset.filter():
#             # print(i.id)
#             # 创建str，如果要加时间的话，就加上下面的代码
#             # str = '{} {}更改了Moderate表的id为{}的信息：已通过，审核成功！'.format(timezone.now(), us, i.id)
#             str = '{}更改了Moderate表的id为{}的信息：已通过，审核成功！'.format(us, i.id)
#             # 插入数据到Log表中
#             ModerateLog.objects.create(record=str)
#
#         # 更新状态和审核
#         rows_upb = queryset.update(status="1", check_value="1")
#         # 如果获取的数是1,则执行下面代码
#         if rows_upb == 1:
#             message_bit = "1个视频"
#         else:
#             message_bit = "%s 个视频" % rows_upb
#         # 通过多少的数据，显示到admin页面上
#         self.message_user(request, "%s 已经通过." % message_bit)
#
#     # 更改Action的内容为通过
#     mak_pub.short_description = "通过"
#
#     # 判断未通过的
#     def mak_pub1(self, request, queryset):
#         # 获取当前的用户
#         us = request.user
#         # 打印未通过的数据
#         for i in queryset.filter():
#             print(i)
#             # 创建str
#             str = '{}更改了Moderate表的id为{}的信息：未通过，审核成功！'.format(us, i.id)
#             # 插入数据到Log表中
#             ModerateLog.objects.create(record=str)
#         # 更新状态和审核
#         rows_upb = queryset.update(status="0", check_value="1")
#         # 如果获取的数是1,则执行下面代码
#         if rows_upb == 1:
#             message_bit = "1个视频"
#         else:
#             message_bit = "%s 个视频" % rows_upb
#         # 通过多少的数据，显示到admin页面上
#         self.message_user(request, "%s 拒绝通过." % message_bit)
#
#     # 更改Action的内容为通过
#     mak_pub1.short_description = "未通过"
#
#     # 重写已经审核过的数据，超级管理员不会通过
#     def get_queryset(self, request):
#         # 获取当前表所有的数据
#         qs = super().get_queryset(request)
#         # 判断是否未超级管理员，如果是就显示所有(已审核和未审核)的信息，不是就显示未审核的信息
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(check_value=0)
