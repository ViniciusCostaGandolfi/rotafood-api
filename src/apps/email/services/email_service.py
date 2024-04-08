from fastapi_mail import FastMail, ConnectionConfig
from config import settings

email_config = ConnectionConfig(
    MAIL_USERNAME = settings.EMAIL_USERNAME,
    MAIL_PASSWORD = settings.EMAIL_PASSWORD,
    MAIL_FROM = settings.EMAIL_FROM,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Email RotaFood",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

email_sandler = FastMail(email_config)