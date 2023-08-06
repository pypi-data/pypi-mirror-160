import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.db import transaction
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

from notification_system.models import OutgoingMessage, NotificationEvent
from notification_system.utils import get_user_common_data

logger = logging.getLogger('notification_system')


@shared_task()
def notification_system_send_internal_message(notification_event_id):
    send_email_status = True
    notification_event = NotificationEvent.objects.prefetch_related('notification_groups__members', 'attachments')
    notification_event = notification_event.prefetch_related('notification_groups')
    notification_event = notification_event.select_related('owner', 'template')
    notification_event = notification_event.get(id=notification_event_id)

    subject = notification_event.get_subject()
    content = notification_event.get_content()
    recipients = notification_event.get_recipients(check_email_isnull=True)

    outgoing_message_objects = []
    for user in recipients:
        context = get_user_common_data(user=user)
        recipient = user.email or ''
        outgoing_message_object = OutgoingMessage(subject=subject, recipient=recipient, context=dict(context),
                                                  content=content, user=user, notification_event=notification_event,
                                                  status=OutgoingMessage.STATUS_SENT,
                                                  outgoing_message_type=OutgoingMessage.TYPE_INTERNAL_MESSAGE)
        outgoing_message_objects.append(outgoing_message_object)

    if outgoing_message_objects:
        try:
            OutgoingMessage.objects.bulk_create(outgoing_message_objects)
        except Exception as e:
            message = _("Error occurred while sending internal messages. error_type: {}, error message: {}"
                        .format(type(e), str(e)))
            logger.error(msg=message)
            send_email_status = False

    return send_email_status


@shared_task(rate_limit=getattr(settings, 'NOTIFICATION_SYSTEM_SEND_EMAIL_RATE_LIMIT', '700/m'))
def notification_system_send_email(subject, recipient, email_from, context, content='', notification_event=None,
                                   user_id=None, smtp_config=None, attachments=None):
    send_email_status = True
    outgoing_message = OutgoingMessage.objects.create(recipient=recipient, subject=subject, context=dict(context),
                                                      content=content, user_id=user_id,
                                                      notification_event_id=notification_event)

    try:
        template_instance = Template(template_string=content)
        context_instance = Context(dict_=context)
        content = template_instance.render(context=context_instance)
        emails = recipient if isinstance(recipient, list) else [recipient]
        smtp_connection = EmailBackend(**smtp_config) if smtp_config else None
        headers = {'outgoing_message_id': outgoing_message.id}
        mail = EmailMultiAlternatives(subject=subject, body=content, from_email=email_from, to=emails, headers=headers,
                                      connection=smtp_connection)
        for attachment in attachments:
            mail.attach_file(path=attachment)

        mail.attach_alternative(content, "text/html")
        mail.send()

        outgoing_message.status = OutgoingMessage.STATUS_SENT

    except Exception as e:
        logger.error(_("Error occurred while sending email. error_type: {}, error message: {}".format(type(e), str(e))))
        send_email_status = False
        outgoing_message.status = OutgoingMessage.STATUS_FAILED
        outgoing_message.error_message = "type: {}\nmessage: {}".format(type(e), str(e))

    outgoing_message.save()
    return send_email_status


@shared_task()
def update_outgoing_message_status(outgoing_message_id, status):
    map_status = {
        'Bounce': OutgoingMessage.STATUS_AMAZON_BOUNCE,
        'Complaint': OutgoingMessage.STATUS_AMAZON_COMPLAINT,
        'Delivery': OutgoingMessage.STATUS_AMAZON_DELIVERY,
        'Send': OutgoingMessage.STATUS_AMAZON_SEND,
        'Reject': OutgoingMessage.STATUS_AMAZON_REJECT,
        'Open': OutgoingMessage.STATUS_AMAZON_OPEN,
        'Click': OutgoingMessage.STATUS_AMAZON_CLICK,
        'Rendering Failure': OutgoingMessage.STATUS_AMAZON_RENDERING_FAILURE,
        'DeliveryDelay': OutgoingMessage.STATUS_AMAZON_DELIVERY_DELAY,
        'Subscription': OutgoingMessage.STATUS_AMAZON_SUBSCRIPTION,
    }

    status = map_status.get(status)
    if (not status) or (not str(outgoing_message_id).isdigit()):
        return False

    with transaction.atomic():
        result = OutgoingMessage.objects.filter(pk=outgoing_message_id).update(status=status)

    return bool(result)
