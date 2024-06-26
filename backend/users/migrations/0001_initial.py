# Generated by Django 4.0.8 on 2023-05-11 16:09

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码')),
                ('image', models.ImageField(default='images/default.png', upload_to='images/%Y/%m/%d/')),
                ('login_status', models.SmallIntegerField(choices=[(0, '在线'), (1, '离线'), (2, '忙碌'), (3, '离开')], default=1, verbose_name='登录状态')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'ipam_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccessTimeOutLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('re_time', models.CharField(max_length=32, verbose_name='请求时间')),
                ('re_user', models.CharField(max_length=32, verbose_name='操作人')),
                ('re_ip', models.CharField(max_length=32, verbose_name='请求IP')),
                ('re_url', models.CharField(max_length=255, verbose_name='请求url')),
                ('re_method', models.CharField(max_length=11, verbose_name='请求方法')),
                ('re_content', models.TextField(null=True, verbose_name='请求参数')),
                ('rp_content', models.TextField(null=True, verbose_name='响应参数')),
                ('rp_code', models.TextField(null=True, verbose_name='响应码')),
                ('user_agent', models.TextField(null=True, verbose_name='请求浏览器')),
                ('access_time', models.IntegerField(verbose_name='响应耗时/ms')),
            ],
            options={
                'verbose_name': '平台超时操作日志表',
                'verbose_name_plural': '平台超时操作日志表',
                'db_table': 'ipam_access_timeout_logs',
            },
        ),
        migrations.CreateModel(
            name='OpLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('re_time', models.CharField(max_length=32, verbose_name='请求时间')),
                ('re_user', models.CharField(max_length=32, verbose_name='操作人')),
                ('re_ip', models.CharField(max_length=32, verbose_name='请求IP')),
                ('re_url', models.CharField(max_length=255, verbose_name='请求url')),
                ('re_method', models.CharField(max_length=11, verbose_name='请求方法')),
                ('re_content', models.TextField(null=True, verbose_name='请求参数')),
                ('rp_content', models.TextField(null=True, verbose_name='响应参数')),
                ('rp_code', models.TextField(null=True, verbose_name='响应码')),
                ('user_agent', models.TextField(null=True, verbose_name='请求浏览器')),
                ('access_time', models.IntegerField(verbose_name='响应耗时/ms')),
            ],
            options={
                'verbose_name': '平台操作日志表',
                'verbose_name_plural': '平台操作日志表',
                'db_table': 'ipam_op_logs',
            },
        ),
        migrations.AddIndex(
            model_name='oplogs',
            index=models.Index(fields=['re_ip'], name='ipam_op_log_re_ip_ae259c_idx'),
        ),
        migrations.AddIndex(
            model_name='oplogs',
            index=models.Index(fields=['re_url'], name='ipam_op_log_re_url_47f179_idx'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
