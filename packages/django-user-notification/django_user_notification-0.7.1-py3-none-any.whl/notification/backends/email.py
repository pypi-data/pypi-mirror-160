import typing
from email.mime.base import MIMEBase

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from notification.backends.base import BaseNotificationBackend, notify
from notification.models import Message


class EmailNotificationBackend(BaseNotificationBackend):
    """
    A backend handle email message
    """

    id = "email"
    content_subtype = "html"

    def make_content(self, title, content, recipients, recipient_field, **kwargs):
        return {
            "subject": title,
            "body": content,
            **kwargs,
        }

    def perform_send(
        self, message: Message, recipients, recipient_field, save, **kwargs
    ):
        """
        For details, see: ...
        """
        email_content = message.content
        for recipient in recipients:
            recipient_email = self.get_recipient(recipient, recipient_field)
            notify_kwargs = {"to": [recipient_email]}
            email = EmailMessage(**notify_kwargs, **email_content)
            email.content_subtype = self.content_subtype
            try:
                email.send()
            except Exception as e:
                self.on_failure(message, recipient, e, save, notify_kwargs)
            else:
                self.on_success(message, recipient, save, notify_kwargs)


def notify_by_email(
    recipients: list[User],
    title: str = None,
    message: str = None,
    context: dict = None,
    template_code: str = None,
    email_field: typing.Union[str, typing.Callable] = "email",
    cc: list[str] = None,
    attachments: list[MIMEBase] = None,
    save=False,
    **kwargs,
):
    """
    Shortcut for email notification
    """
    message_kwargs = {
        "cc": cc,
        "attachments": attachments,
    }

    return notify(
        recipients,
        title=title,
        message=message,
        context=context,
        template_code=template_code,
        backends=(EmailNotificationBackend,),
        save=save,
        recipient_field=email_field,
        message_kwargs=message_kwargs,
        **kwargs,
    )
