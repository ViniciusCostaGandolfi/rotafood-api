from fastapi_mail import FastMail, ConnectionConfig
from api.config.env_settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.EMAIL_USERNAME,
    MAIL_PASSWORD = settings.EMAIL_PASSWORD,
    MAIL_FROM = settings.EMAIL_USERNAME,
    MAIL_PORT = int(settings.EMAIL_PORT),
    MAIL_SERVER = settings.EMAIL_SERVER,
    MAIL_FROM_NAME="Email RotaFood",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

email_sandler = FastMail(conf)