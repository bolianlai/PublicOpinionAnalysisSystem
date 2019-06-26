import os
import sys
import django

import logging

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    # CHANGED manage.py will use development settings by
    # default. Change the DJANGO_SETTINGS_MODULE environment variable
    # for using the environment specific settings file.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage.settings")

    django.setup()
    #from django.contrib.auth.models import User
    from django.contrib.auth import get_user_model

    username = 'bolian'
    password = '123456'
    email = 'bolian@qq.com'

    User = get_user_model()
    if User.objects.filter(username = username).count() == 0:
        User.objects.create_superuser(username = username, email = email, password = password)
        logger.error('管理用户创建成功: username: bolian   password:123456   email:bolian@qq.com')
    else:
        logger.error('管理用户已经存在：bolian')
