from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from configs import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# import ssl
#
# ssl._create_default_https_context = ssl._create_unverified_context

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)


mail = FastMail(conf)


async def simple_send(
    emails: list[EmailStr],
    body: str,
    subject: str = "Fastapi-Mail module",
    subtype: MessageType = MessageType.html,
    *args,
    **kwargs
):
    message = MessageSchema(subject=subject, recipients=emails, body=body, subtype=subtype, *args, **kwargs)
    await mail.send_message(message)
    logger.info("发送邮件成功!")


if __name__ == "__main__":
    # fastapi_mail 文档地址: https://sabuhish.github.io/fastapi-mail/
    html = """
    <p>Thanks for using Fastapi-mail</p> 
    """
    import asyncio

    asyncio.run(simple_send(emails=["zhiyuan597@126.com"], body=html, subject="haha4h"))
