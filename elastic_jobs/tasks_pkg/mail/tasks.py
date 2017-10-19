# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import types
from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class SenderMail(object):
    """ 基于宙斯盾(Aegis)平台的用户注册邮件发送系统 """

    def __init__(self, subject, message, from_email=None, recipient_list=None):
        self.subject = subject
        self.message = message
        self.from_email = from_email or settings.EMAIL_HOST_USER

        assert not isinstance(recipient_list, types.NoneType), "recipient_list argument must a list and not empty"
        self.recipient_list = [recipient_list] if isinstance(recipient_list, types.StringType) else list(recipient_list)

    def send(self):
        response = {'isSuccess': False, 'message': ''}

        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
            )
        except SMTPException as e:
            response['message'] = str(e)
        else:
            response['isSuccess'] = True
            response['message'] = 'send mail is successful'

        return response


@shared_task
def send_mail_by_celery(subject, message, recipient_list):
    logger.info('Send Register checking code mail!')

    SenderMail(
        subject=subject,
        message=message,
        recipient_list=recipient_list
    ).send()

    return dict(isSuccess=True, message='send mail is successful')

