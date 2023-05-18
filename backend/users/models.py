from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
    login_status_ = (
        (0, '在线'),
        (1, '离线'),
        (2, '忙碌'),
        (3, '离开'),
    )
    nick_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='昵称')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', default='images/default.png', max_length=100)
    login_status = models.SmallIntegerField(choices=login_status_, default=1, verbose_name='登录状态')

    def get_login_status(self):
        return self.login_status

    class Meta:
        db_table = 'ipam_user'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class OpLogs(models.Model):
    '''操作日志表'''
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    rp_code = models.TextField(null=True, verbose_name='响应码')
    user_agent = models.TextField(null=True, verbose_name='请求浏览器')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        indexes = [
            models.Index(fields=['re_ip'], ),
            models.Index(fields=['re_url'], ),
            # models.Index(fields=['user_agent'], ),
        ]
        db_table = 'ipam_op_logs'
        verbose_name = '平台操作日志表'
        verbose_name_plural = '平台操作日志表'


class AccessTimeOutLogs(models.Model):
    '''超时操作日志表'''
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    rp_code = models.TextField(null=True, verbose_name='响应码')
    user_agent = models.TextField(null=True, verbose_name='请求浏览器')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'ipam_access_timeout_logs'
        verbose_name = '平台超时操作日志表'
        verbose_name_plural = '平台超时操作日志表'


