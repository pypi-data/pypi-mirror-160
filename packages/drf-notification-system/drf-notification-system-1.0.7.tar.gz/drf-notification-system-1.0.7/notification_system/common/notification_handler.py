import abc

from django.conf import settings

from notification_system.tasks import notification_system_send_email


class NotificationHandler(metaclass=abc.ABCMeta):
    TYPE_EMAIL = 1
    TYPE_INTERNAL_MESSAGE = 2
    EMAIL_NOTIFICATION_QUEUE_NAME = getattr(settings, 'EMAIL_NOTIFICATION_QUEUE_NAME', 'send_email_notification')
    INTERNAL_MESSAGE_NOTIFICATION_QUEUE_NAME = getattr(settings, 'INTERNAL_MESSAGE_NOTIFICATION_QUEUE_NAME',
                                                       'send_internal_message_notification')

    @abc.abstractmethod
    def send(self):
        pass


class EmailNotificationHandler(NotificationHandler):

    def __init__(self, subject, recipient, email_from, context, notification_type=NotificationHandler.TYPE_EMAIL,
                 content='', notification_event=None, user_id=None, smtp_config=None, attachments=None):
        """
        :param subject: This field specifies the notification subject
        :type subject: str
        :param recipient: The recipient of the notification is specified in this field
        :type recipient: str
        :param email_from: In this field, you specify the email address of the sender
        :type email_from: str
        :param context: This field specifies extra info for notification
        :type context: dict
        :param content: This field specifies mail template.
        :type content: str
        :param notification_type: This field specifies the notification type
        :type notification_type: int
        :param notification_event: This field specifies the notification_event id
        :type notification_event: int
        :param user_id: This field specifies the user_id
        :type user_id: int
        :param smtp_config: This field specifies the smtp_config
        :type smtp_config: dict
        :param attachments: The attachments of this notification are specified in this field
        :type attachments: list
        """
        self.subject = subject
        self.recipient = recipient
        self.email_from = email_from
        self.context = context
        self.content = content
        self.notification_event = notification_event
        self.user_id = user_id
        self.smtp_config = smtp_config
        self.attachments = attachments
        self.notification_type = notification_type

    def send(self):
        kwargs = {
            'subject': self.subject,
            'recipient': self.recipient,
            'email_from': self.email_from,
            'context': self.context,
            'content': self.content,
            'notification_event': self.notification_event,
            'user_id': self.user_id,
            'smtp_config': self.smtp_config,
            'attachments': self.attachments,
        }
        notification_system_send_email.apply_async(kwargs=kwargs, queue=self.EMAIL_NOTIFICATION_QUEUE_NAME)


class InternalMessageNotificationHandler(NotificationHandler):

    def __init__(self, subject, recipients, context, notification_event, content, user_id,
                 notification_type=NotificationHandler.TYPE_INTERNAL_MESSAGE):
        """
        :param subject: This field specifies the notification subject
        :type subject: str
        :param recipients: The recipients of the notification is specified in this field
        :type recipients: list
        :param context: This field specifies extra info for notification
        :type context: dict
        :param content: This field specifies mail template.
        :type content: str
        :param notification_type: This field specifies the notification type
        :type notification_type: int
        :param notification_event: This field specifies the notification_event id
        :type notification_event: int
        :param user_id: This field specifies the user_id
        :type user_id: int
        """
        self.subject = subject
        self.recipients = recipients
        self.context = context
        self.content = content
        self.notification_event = notification_event
        self.user_id = user_id
        self.notification_type = notification_type

    def send(self):
        pass
