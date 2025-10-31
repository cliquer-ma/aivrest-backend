from django.apps import apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery import shared_task

from datetime import datetime, timedelta

@shared_task
def update_competitions_status():
    CompetitionModel = apps.get_model("competitions", "Competition")
    competitions     = CompetitionModel.objects.filter()

    for competition in competitions:
        pass

