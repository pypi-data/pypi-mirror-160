import typing

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from notification.backends.base import BaseNotificationBackend, notify
from notification.models import Message


class DingTalkChatBotNotificationBackend(BaseNotificationBackend):
    """
    A backend handle dingtalk chatbot message.
    For details, see: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    """

    id = "dingtalkchatbot"
    default_msgtype = "markdown"

    def __init__(self, *args, webhook=None, **kwargs):
        try:
            self.notification_settting = settings.DJANGO_USER_NOTIFICATION[self.id]
        except (AttributeError, KeyError):
            raise ImproperlyConfigured(
                "'DJANGO_USER_NOTIFICATION[{}]' must be set in settings.py".format(
                    self.id
                )
            )

        self.webhook = webhook or self.notification_settting.get("webhook")

        super().__init__(*args, **kwargs)

    def make_content(
        self, title, content, recipients, recipient_field, **kwargs
    ) -> dict:
        at_mobiles = kwargs.get("at_mobiles", [])
        if not at_mobiles and recipients and recipient_field:
            at_mobiles = [
                self.get_recipient(recipient, recipient_field)
                for recipient in recipients
            ]

        msgtype = kwargs.get("msgtype", self.default_msgtype)
        body = {
            "msgtype": msgtype,
            msgtype: {"title": title, "text": content},
        }

        if kwargs.get("at_all"):
            body["at"] = {"isAtAll": True}
        elif at_mobiles:
            format_at_str = ("@" + str(mobile) for mobile in at_mobiles)
            content = " ".join(format_at_str) + "\n\n" + content
            body[msgtype]["text"] = content
            body["at"] = {"atMobiles": at_mobiles}

        return body

    def perform_send(
        self, message: Message, recipients, recipient_field, save, **kwargs
    ) -> None:
        """
        For details, see: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
        """
        try:
            resp = requests.post(self.webhook, json=message.content)
            resp.raise_for_status()
            assert resp.json()["errcode"] == 0, resp.json()["errmsg"]
        except Exception as e:
            self.on_failure(message, "dingtalk chatbot", e, save=save)
        else:
            self.on_success(message, "dingtalk chatbot", save)


def notify_by_dingtalk_chatbot(
    recipients: list[User] = None,
    title: str = "notify",
    message: str = None,
    context: dict = None,
    template_code: str = None,
    msgtype: str = "markdown",
    at_all: bool = False,
    at_mobiles: list[str] = None,
    phone_field: typing.Union[str, typing.Callable] = None,
    webhook: str = None,
    save: bool = False,
    **kwargs,
):
    """
    Shortcut for dingtalk chatbot notification
    """
    message_kwargs = {
        "msgtype": msgtype,
        "at_all": at_all,
    }

    if at_mobiles:
        message_kwargs["at_mobiles"] = at_mobiles

    return notify(
        recipients,
        title=title,
        message=message,
        context=context,
        template_code=template_code,
        backends=(DingTalkChatBotNotificationBackend,),
        save=save,
        recipient_field=phone_field,
        message_kwargs=message_kwargs,
        webhook=webhook,
        **kwargs,
    )
