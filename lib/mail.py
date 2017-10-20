# -*- coding: utf-8 -*-

import string
from random import sample

from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings


def get_validation_code():
    digits_length = 2
    uppercase_length = 4
    lowercase_length = 3
    total_length = digits_length + uppercase_length + lowercase_length

    digit = sample(string.digits, digits_length)
    uppercase = sample(string.uppercase, uppercase_length)
    lowercase = sample(string.lowercase, lowercase_length)

    suffix = sample(string.letters + string.digits, 3)
    verify_code = sample(digit + uppercase + lowercase, total_length)

    return ''.join(verify_code + suffix)


class SenderMail(object):
    """ 通用宙斯盾(Aegis)平台的用户注册邮件发送系统
        一般适合小文本邮件发送，大文件或附件不建议使用.
     """

    def __init__(self, subject, message, from_email=None, recipient_list=None):
        self.subject = subject
        self.message = message
        self.from_email = from_email or settings.EMAIL_HOST_USER

        assert isinstance(recipient_list, (list, tuple)), "recipient_list argument must a list and not empty"
        self.recipient_list = recipient_list

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


class DefinedSenderMail(object):
    """ 自定义邮件发送类 """


if __name__ == "__main__":
    pass

