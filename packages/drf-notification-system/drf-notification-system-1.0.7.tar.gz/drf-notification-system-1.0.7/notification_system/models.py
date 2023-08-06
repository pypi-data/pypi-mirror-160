from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from notification_system.managers import ActiveManager
from notification_system.validators import validate_file_extension, validate_file_size

User = get_user_model()


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        abstract = True


class SmtpProvider(BaseModel):
    provider_name = models.CharField(verbose_name=_('provider name'), max_length=255)
    email_host = models.CharField(verbose_name=_('email host'), max_length=255)
    email_host_user = models.CharField(verbose_name=_('email host user'), max_length=255)
    email_host_password = models.CharField(verbose_name=_('email host password'), max_length=1024)
    email_port = models.CharField(verbose_name=_('email port'), max_length=255, default=587)
    email_from = models.CharField(max_length=255, verbose_name=_('email from'), blank=True,
                                  help_text=mark_safe("Mail from <'mail@mail.com'>"))
    email_timeout = models.PositiveSmallIntegerField(verbose_name=_('email timeout'), blank=True, null=True)
    email_use_tls = models.BooleanField(verbose_name=_('email use tls'), default=False)
    email_use_ssl = models.BooleanField(verbose_name=_('email use ssl'), default=False)
    email_ssl_keyfile = models.TextField(verbose_name='email ssl keyfile', blank=True)
    email_ssl_certfile = models.TextField(verbose_name='email ssl certfile', blank=True)
    users = models.ManyToManyField(to=User, verbose_name=_('user access'), related_name='users', blank=True)
    is_active = models.BooleanField(verbose_name=_('is active?'), default=True)

    objects = models.Manager()
    actives = ActiveManager()

    def __str__(self):
        return "{} - {}".format(self.id, self.provider_name)

    def clean(self):
        if self.email_use_ssl and self.email_use_tls:
            raise ValidationError(
                _("email_use_tls/email_use_ssl are mutually exclusive, so only set one of those settings to True."))

    def get_smtp_config(self):
        return {
            "host": self.email_host,
            "username": self.email_host_user,
            "password": self.email_host_password,
            "port": self.email_port,
            "use_tls": self.email_use_tls,
            "use_ssl": self.email_use_ssl,
            "timeout": self.email_timeout,
            "ssl_keyfile": self.email_ssl_keyfile,
            "ssl_certfile": self.email_ssl_certfile,
        }


class NotificationGroup(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    owner = models.ForeignKey(to=User, verbose_name=_('owner'), related_name='notification_groups',
                              on_delete=models.PROTECT)
    members = models.ManyToManyField(to=User, verbose_name=_('members'), related_name='members', blank=True)
    is_active = models.BooleanField(verbose_name=_('is active?'), default=True)

    objects = models.Manager()
    actives = ActiveManager()

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


class EmailTemplate(BaseModel):
    title = models.CharField(verbose_name=_('template title'), max_length=255)
    subject = models.CharField(verbose_name=_('subject'), max_length=255)
    content = models.TextField(verbose_name=_('content'), blank=True)
    owner = models.ForeignKey(to=User, verbose_name=_('owner'), related_name='email_templates',
                              on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name=_('is active?'), default=True)

    objects = models.Manager()
    actives = ActiveManager()

    def __str__(self):
        return "{} - {}".format(self.id, self.title)


class NotificationEvent(BaseModel):
    TYPE_EMAIL = 1
    TYPE_INTERNAL_MESSAGE = 2

    TYPE_CHOICES = (
        (TYPE_EMAIL, _('Email')),
        (TYPE_INTERNAL_MESSAGE, _('Internal message')),
    )

    title = models.CharField(verbose_name=_('notification events title'), max_length=255)
    smtp_provider = models.ForeignKey(to=SmtpProvider, verbose_name=_('smtp provider'), on_delete=models.PROTECT,
                                      related_name='notification_events', null=True, blank=True)
    owner = models.ForeignKey(to=User, verbose_name=_('owner'), related_name='notification_events',
                              on_delete=models.PROTECT)
    notification_groups = models.ManyToManyField(to=NotificationGroup, verbose_name=_('notification groups'),
                                                 blank=True, related_name='notification_events')
    template = models.ForeignKey(to=EmailTemplate, on_delete=models.PROTECT, related_name='notification_events',
                                 null=True, blank=True,
                                 help_text=_("If template is selected, HTML message and subject fields will not be used"
                                             "- they will be populated from template"))
    notification_event_type = models.PositiveSmallIntegerField(verbose_name=_('type'), choices=TYPE_CHOICES,
                                                               default=TYPE_EMAIL)
    recipients = models.ManyToManyField(to=User, verbose_name=_('members'), related_name='recipients', blank=True)
    subject = models.CharField(verbose_name=_('subject'), max_length=255, blank=True)
    content = models.TextField(verbose_name=_('content'), blank=True)
    is_active = models.BooleanField(verbose_name=_('is active?'), default=True)

    objects = models.Manager()
    actives = ActiveManager()

    def __str__(self):
        return "{} - {}".format(self.id, self.title)

    def save(self, *args, **kwargs):
        self.smtp_provider = self.smtp_provider if self.notification_event_type == self.TYPE_EMAIL else None

        super().save(*args, **kwargs)

    def clean(self):
        if self.notification_event_type == self.TYPE_EMAIL and not self.smtp_provider:
            raise ValidationError(_("For this type, the SMTP provider field must be filled in."))

    def get_content(self):
        return self.content if not self.template else self.template.content

    def get_subject(self):
        return self.subject if not self.template else self.template.subject

    def get_recipients(self, check_email_isnull=False):
        recipients = self.recipients.all()

        for notification_group in self.notification_groups.filter(is_active=True):
            recipients = recipients | notification_group.members.all()

        filter_params = {
            "email__isnull": False,
        }
        if check_email_isnull:
            filter_params.pop('email__isnull', None)

        return recipients.filter(is_active=True, **filter_params).distinct()


class Attachment(BaseModel):
    file = models.FileField(verbose_name=_('file'), upload_to='notification_system/attachment/file/',
                            validators=[validate_file_extension, validate_file_size])
    notification_event = models.ForeignKey(to=NotificationEvent, verbose_name=_('notification event'),
                                           related_name='attachments', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class Media(BaseModel):
    file = models.FileField(verbose_name=_('file'), upload_to='notification_system/media/file/',
                            validators=[validate_file_extension, validate_file_size])
    owner = models.ForeignKey(to=User, verbose_name=_('owner'), related_name='media', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')

    def __str__(self):
        return str(self.id)


class OutgoingMessage(BaseModel):
    TYPE_EMAIL = 1
    TYPE_INTERNAL_MESSAGE = 2

    TYPE_CHOICES = (
        (TYPE_EMAIL, _('Email')),
        (TYPE_INTERNAL_MESSAGE, _('Internal message')),
    )

    STATUS_SENT = 1
    STATUS_PENDING = 2
    STATUS_FAILED = 3
    STATUS_AMAZON_BOUNCE = 4
    STATUS_AMAZON_COMPLAINT = 5
    STATUS_AMAZON_DELIVERY = 6
    STATUS_AMAZON_SEND = 7
    STATUS_AMAZON_REJECT = 8
    STATUS_AMAZON_OPEN = 9
    STATUS_AMAZON_CLICK = 10
    STATUS_AMAZON_RENDERING_FAILURE = 11
    STATUS_AMAZON_DELIVERY_DELAY = 12
    STATUS_AMAZON_SUBSCRIPTION = 13

    STATUS_CHOICES = [
        (STATUS_FAILED, _('Failed')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_SENT, _('Sent')),
        (STATUS_AMAZON_BOUNCE, _('Bounce')),
        (STATUS_AMAZON_COMPLAINT, _('Complaint')),
        (STATUS_AMAZON_DELIVERY, _('Delivery')),
        (STATUS_AMAZON_SEND, _('Send')),
        (STATUS_AMAZON_REJECT, _('Reject')),
        (STATUS_AMAZON_OPEN, _('Open')),
        (STATUS_AMAZON_CLICK, _('Click')),
        (STATUS_AMAZON_RENDERING_FAILURE, _('Rendering Failure')),
        (STATUS_AMAZON_DELIVERY_DELAY, _('Delivery Delay')),
        (STATUS_AMAZON_SUBSCRIPTION, _('Subscription')),
    ]

    user = models.ForeignKey(to=User, verbose_name=_('user'), related_name='outgoing_messages', null=True, blank=True,
                             on_delete=models.PROTECT)
    notification_event = models.ForeignKey(to=NotificationEvent, verbose_name=_('notification event'), null=True,
                                           blank=True, related_name='outgoing_messages', on_delete=models.PROTECT)
    recipient = models.CharField(verbose_name=_('recipient'), max_length=255, blank=True, db_index=True)
    subject = models.CharField(verbose_name=_('subject'), max_length=255, blank=True)
    content = models.TextField(verbose_name=_('message content'), blank=True)
    context = models.TextField(verbose_name=_('message context'), blank=True)
    error_message = models.TextField(verbose_name=_('error message'), blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS_CHOICES, default=STATUS_PENDING)
    outgoing_message_type = models.PositiveSmallIntegerField(verbose_name=_('type'), choices=TYPE_CHOICES,
                                                             default=TYPE_EMAIL)

    def __str__(self):
        return "{} - {}".format(self.id, self.subject)
