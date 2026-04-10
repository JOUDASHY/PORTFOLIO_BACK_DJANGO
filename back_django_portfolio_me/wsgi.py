"""
WSGI config for back_django_portfolio_me project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')

# Guard against wfastcgi double-init (populate() isn't reentrant)
if not django.apps.apps.ready:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
else:
    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()