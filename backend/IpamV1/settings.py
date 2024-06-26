"""
Django settings for IpamV1 project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path
from confload.confload import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# If You Have APP Dir
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1hoyyz)v$99z2r8oxf&p&v!9(y$9vijy28m2(m$y!xuq%kv2#l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'None'
ALLOWED_HOSTS = ["*"]
# 设置项是否开启URL访问地址后面不为/跳转至带有/的路径
APPEND_SLASH = True

# # 用户自定义配置
# if os.path.exists("{}/{}/{}".format(BASE_DIR, "IpamV1", "conf.py")):
#     from .conf import *
# else:
#     raise RuntimeError("没有找到conf.py的配置信息")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IpamV1.settings")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'rest_framework.authtoken',
    'import_export',
    'reversion',
    'open_ipam',
    'users',
    # 'django_celery_beat'
]
# 取消验证-对接微服务
REST_FRAMEWORK = {
    "DATE_FORMAT": "%Y-%m-%d",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.DjangoModelPermissions',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'utils.authentication.ExpiringTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.LogMiddleware.PlatformOperationLogs',
    'middlewares.CrossMiddleware.CorsMiddleWare'
]

# django    报错 because it set 'X-Frame-Options' to 'deny'.
# X_FRAME_OPTIONS = 'SAMEORIGIN'
#
# MIDDLEWARE += ['middlewares.LogMiddleware.PlatformOperationLogs', 'middlewares.CrossMiddleware.CorsMiddleWare']

ROOT_URLCONF = 'IpamV1.urls'

STATICFILES_FINDERS = (
    # "django.contrib.staticfiles.finders.FileSystemFinder",
    # # causes verbose duplicate notifications in django 1.9
    # "django.contrib.staticfiles.finders.AppDirectoriesFinder",

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',

)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'openwisp_utils.loaders.DependencyLoader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 处理静态问题件
                'django.template.context_processors.media'
                # 'openwisp_utils.admin_theme.context_processor.menu_groups',
            ],
        },
    },
]

WSGI_APPLICATION = 'IpamV1.wsgi.application'

IMPORT_EXPORT_USE_TRANSACTIONS = True
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
# 隐藏右侧SimpleUI广告链接和使用分析
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
# 重载AUTH_USER_MODEL
AUTH_USER_MODEL = 'users.UserProfile'

AUTHENTICATION_BACKENDS = (
    # "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
    # "guardian.backends.ObjectPermissionBackend",  # 这是guardian的
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# STATIC_ROOT = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Restful token 有效时间60分钟
REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES = 60 * 8

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
SERVER_LOGS_FILE = os.path.join(BASE_DIR, "logs", "server.log")
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

CONSOLE_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(message)s",
        },
        "simple": {
            "format": "%(levelname)s %(message)s",

        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',  # 过滤器，只有当setting的DEBUG = True时生效
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',  # 此过滤器仅在settings.DEBUG为False时传递记录
        },
    },
    "handlers": {
        "console": {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'server': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "server.log"),  # 日志文件
            # 'filters': ['require_debug_true'],
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "request.log"),
            'maxBytes': 1024 * 1024 * 50,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        # 'db_backends': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(BASE_LOG_DIR, "dbbackends.log"),
        #     'maxBytes': 1024 * 1024 * 50,  # 5 MB
        #     'backupCount': 5,
        #     'formatter': 'verbose',
        # },
        'ipam': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "ipam.log"),
            'maxBytes': 1024 * 1024 * 50,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },

    "loggers": {
        '': {
            'handlers': ['server', 'console'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        "django": {
            "handlers": ["server", "console"],
            "level": 'DEBUG',
            "propagate": False,
        },
        'django.request': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        # 'django.db.backends': {
        #     'handlers': ['db_backends', 'console'],  # 与代码与数据库的交互有关的消息。例如，请求执行的每个应用程序级SQL语句都在 DEBUG该记录器级别记录。
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        'ipam': {
            'handlers': ['ipam', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'server': {
            'handlers': ['server'],
            'level': 'DEBUG',
            'propagate': False
        },
    },

}

DATABASES = {
    'default': {
        'NAME': config.mysql_db,
        'ENGINE': 'django.db.backends.mysql',
        'USER': config.mysql_user,
        'HOST': config.mysql_host,
        'PASSWORD': config.mysql_password,
        'PORT': config.mysql_port,
        'CONN_MAX_AGE': 21600,
        'ATOMIC_REQUESTS': True,
        'TEST_CHARSET': 'utf8mb4',
        'TEST_COLLATION': 'utf8mb4_general_ci',
        'OPTIONS': {
            # 'charset': 'utf8mb4',
        }
    },
}
