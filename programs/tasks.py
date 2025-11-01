from django.apps import apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery import shared_task

from datetime import datetime, timedelta

import requests

from programs.models import (
    Program,
    ProgramType
)

@shared_task
def generate_workout_plan(ai_coach, user_id: str, messages_history: list, user_profile: dict):


    json_content = {
        'user_profile'  : user_profile,
        'messages_history': messages_history,
    }

    response_data   = ai_coach._call_agent(json_content, 'workout_architect_agent')

    if response_data:
        program_title       = response_data.get('program_title')
        program_summary     = response_data.get('program_summary')
        weekly_schedule     = response_data.get('weekly_schedule')

        workout_plan           = {
            "program_title": program_title,
            "program_summary": program_summary,
            "weekly_schedule": weekly_schedule
        }
        print(f"✅ Workout plan generated: {program_title}")

        # _save_program_to_firebase("sport", workout_plan, user_id)

        Program.objects.create(
            user          = user_id,
            program_type  = "sport",
            title         = program_title,
            content       = weekly_schedule,
        )

        return True
