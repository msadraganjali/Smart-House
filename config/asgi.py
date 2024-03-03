"""
Generate by django-system-core-configration-asgi-packages-app-asgi using Django 4.2 System conf co.

ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
        # frestadan response
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
