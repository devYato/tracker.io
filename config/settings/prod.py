from .base import *

DEBUG = False

# Segurança mínima (reforçar no Deployment Checklist)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True