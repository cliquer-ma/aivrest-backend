from django.apps import apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery import shared_task

from datetime import datetime, timedelta

import requests

@shared_task
def send_email(subject, template, data, email_address):
    sender_email = "contact@whappify.com"
    html_content  = render_to_string(template, data)
    email         = EmailMessage(subject, html_content, sender_email, [email_address,])
    email.content_subtype = 'html'
    email.send()
