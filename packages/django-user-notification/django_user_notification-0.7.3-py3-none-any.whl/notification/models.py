from django.conf import settings
from django.db import models
from django.template import Context, Template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2

    PUSH_STATE_CHOICE = (
        (PENDING, _("Pending")),
        (SUCCESS, _("Success")),
        (FAILED, _("Failure")),
    )

    has_read = models.BooleanField(verbose_name=_("Read Or Not"), default=False)
    is_ignored = models.BooleanField(verbose_name=_("Ignored Or Not"), default=False)
    push_state = models.PositiveIntegerField(choices=PUSH_STATE_CHOICE, default=PENDING)
    to = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Receiver"), on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        "Message",
        verbose_name=_("Message"),
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notify_kwargs = models.JSONField(
        verbose_name=_("Notify Kwargs"), blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    objects = models.Manager()

    class Meta:
        verbose_name = _("Notification")
        db_table = "notification"


class MessageTemplate(models.Model):
    """
    Message template
    """

    name = models.CharField(max_length=64, verbose_name=_("Template Name"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    code = models.CharField(max_length=4, verbose_name=_("Template Code"), unique=True)
    title = models.CharField(
        max_length=64, verbose_name=_("Message Title"), null=True, blank=True
    )
    content = models.TextField(verbose_name=_("Template Content"))
    backend_kwargs = models.JSONField(
        verbose_name=_("Backend Kwargs"), blank=True, null=True
    )
    message_kwargs = models.JSONField(
        verbose_name=_("Message Kwargs"), null=True, blank=True
    )

    objects = models.Manager()

    def __str__(self):
        return self.title

    def render(self, context):
        """
        Render message
        """
        try:
            template = Template(self.content)
            return template.render(Context(context))
        except Exception:
            raise ValueError(_("Render message failed!"))

    class Meta:
        verbose_name = _("Message Template")
        db_table = "message_template"


class Message(models.Model):
    """
    Message
    """

    title = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("Title")
    )
    mark = models.CharField(
        max_length=64,
        verbose_name=_("Message Mark"),
        null=True,
        blank=True,
        db_index=True,
    )
    msg_type = models.CharField(
        max_length=64, verbose_name=_("Message Type"), db_index=True
    )
    content = models.TextField(verbose_name=_("Content"), null=True, blank=True)
    template = models.ForeignKey(
        MessageTemplate,
        verbose_name=_("Template"),
        db_constraint=False,
        null=True,
        on_delete=models.CASCADE,
    )
    render_kwargs = models.JSONField(
        verbose_name=_("Render Kwargs"), null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_content(self):
        if self.template:
            return self.template.render(self.render_kwargs)
        return self.content

    def read(self, user):
        """
        Set message as read
        """
        self.notification_set.filter(to=user).update(  # noqa
            has_read=True, updated_at=timezone.now()
        )

    def ignore(self, user):
        """
        Set message as ignored
        """
        self.notification_set.filter(to=user).update(  # noqa
            is_ignored=True, updated_at=timezone.now()
        )

    def resend(self, users=None):
        # try:
        #     notification_backend = get_notification_backend(self.msg_type)
        # except Exception:
        #     raise TypeError("Notification for: {} not found".format(self.msg_type))
        raise NotImplementedError

    class Meta:
        verbose_name = _("Message")
        db_table = "message"
