
STATIC_URL = ''
SECRET_KEY = ''
SMTP_HOST = ''
SMTP_USER = ''
SMTP_PASS = ''
SMTP_PORT = 465
SMTP_TLS = True
EMAIL_SUBJECT = 'KontrolVM Contact Page'

try:
    from local_settings import *
except:
    pass
