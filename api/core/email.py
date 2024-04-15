from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = "contato.rotafood@gmail.com",
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', ''),
    MAIL_FROM = "contato.rotafood@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Email RotaFood",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

email_sandler = FastMail(conf)