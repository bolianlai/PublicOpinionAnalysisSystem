import os
def get_dev_config(LOGFILE_ROOT):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  # 日志格式
        },
        'filters': {
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'encoding': 'utf8',
                'filename':  os.path.join(LOGFILE_ROOT, 'all.log'),  # 日志输出文件
                'maxBytes': 1024*1024*5,  # 文件大小
                'backupCount': 5,  # 备份份数
                'formatter': 'standard',  # 使用哪种formatters日志格式

            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':   os.path.join(LOGFILE_ROOT, 'error.log'),
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf8',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'request_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':   os.path.join(LOGFILE_ROOT, 'request.log'),
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf8',
            },
            'scprits_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':  os.path.join(LOGFILE_ROOT, 'script.log'),
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf8',
            },
            'template_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':  os.path.join(LOGFILE_ROOT, 'template.log'),
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf8',
            },
            'apps_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':  os.path.join(LOGFILE_ROOT, 'apps.log'),
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf8',
            }
        },
        'loggers': {
            'apps': {
                'handlers': ['apps_handler', 'console'],
                'level': 'DEBUG',
                'propagate': False
            },
            'django': {
                'handlers': ['default', 'console', 'error'],
                'level': 'DEBUG',
                'propagate': False
            },
            'django.request': {
                'handlers': ['request_handler'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['scprits_handler'],
                'level': 'DEBUG',
                'propagate': False
            },
            'django.template': {
                'handlers': ['template_handler'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }

    return LOGGING
