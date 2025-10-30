
import google.genai as genai
from google.genai import types

import json
import string
import random

from copy import deepcopy
from datetime import datetime

from presets.agents import (
    AGENTS
)

class AIFitnessCoach:

    def __init__(self, api_key: str, min_score_threshold=50, conversational_style=75, sarcasm_level=1):

        if not api_key:
            raise ValueError("API key is required to initialize the AIFitnessCoach.")

        self.api_key                = api_key
        self.API_URL                = ""
        self.client                 = genai.Client(api_key=api_key)
        self.MIN_SCORE_THRESHOLD    = min_score_threshold
        self.CONVERSATIONAL_STYLE   = conversational_style
        self.SARCASM_LEVEL          = sarcasm_level

        self._USER_PROFILE_SCHEMA   = {
            "goal": None, "sex": None, "age": None, "weight": None, "height": None,
            "measurements": {"waist": None, "hips": None, "chest": None},
            "activity_level": None, "body_type": None, "sleep_quality": None,
            "stress_level": None, "allergies": [], "illnesses": [],
            "physical_limitations": [], "available_equipment": [],
            "workout_time_preference": None, "food_likes": [], "food_dislikes": [],
            "regimes": [],
            "generated": False
        }
        self._METRIC_WEIGHTS        = {
            "goal": 3, "sex": 3, "age": 3, "weight": 3, "height": 3, "activity_level": 3,

            "allergies": 2, "illnesses": 2, "physical_limitations": 2, "available_equipment": 2,

            "measurements": 1, "body_type": 1, "sleep_quality": 1, "stress_level": 1,
            "workout_time_preference": 1, "food_likes": 1, "food_dislikes": 1, "regimes": 1
        }
        self.TOTAL_POSSIBLE_SCORE   = sum(weight * 10 for weight in self._METRIC_WEIGHTS.values())

        self.user_profile           = deepcopy(self._USER_PROFILE_SCHEMA)
        self.deep_user_profile      = deepcopy(self._USER_PROFILE_SCHEMA)
        self.quality_score          = 0
        self.plan_duration_weeks    = None
        self.duration_explanation   = None
        self.workout_plan           = None
        self.nutrition_plan         = None
        self.threshold_met          = False
        self.program_generation_started = False  # Track if generation has started

    def get_user_profile_schema(self):
        return self._USER_PROFILE_SCHEMA

    def _validate_user_profile(self, user_profile: dict) -> bool:
        valid = True
        for key, value in user_profile.items():
            found = False
            for k, v in self._USER_PROFILE_SCHEMA.items():
                continue

        return valid

    def _init_user_profile(self, user_profile: dict):
        
        if not user_profile:
            raise ValueError("User profile is required")

        # validate user_profile against schema
        # if not self._validate_user_profile(user_profile):
        #     raise ValueError("Invalid user profile")

        self.user_profile       = deepcopy(user_profile)
        self.deep_user_profile  = deepcopy(user_profile)
        self.quality_score      = self._calculate_quality_score()
        return True

    def _generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for i in range(length))
        return random_string

    def _calculate_quality_score(self) -> float:
        if not self.user_profile: return 0.0
        current_user_score = 0
        for key, base_weight in self._METRIC_WEIGHTS.items():
            field = self.user_profile.get(key)
            if not field: continue

            max_category_score = base_weight * 10

            if isinstance(field, list):
                if len(field) > 0:
                    current_user_score += max_category_score
            elif isinstance(field, str) and field != "":
                current_user_score += max_category_score

        return (current_user_score / self.TOTAL_POSSIBLE_SCORE) * 100

    def _call_agent(self, json_content: object, agent_id: str):

        agent               = AGENTS.get(agent_id)

        contents        = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=json.dumps(json_content)
                    ),
                ],
            ),
        ]
        content_config  = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=agent.get('thinking_budget'),
            ),
            response_mime_type  = agent.get('response_mime_type'),
            response_schema     = agent.get('genai_response_schema'),
            system_instruction  = [
                types.Part.from_text(
                    text=agent.get('system_instructions')
                ),
            ],
        )
        response        = self.client.models.generate_content(
            model=agent.get('model'),
            contents=contents,
            config=content_config,
        )

        try:
            response = json.loads(response.text)
            return response
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None


    def _call_chat_agent(self, message: str, messages_history: list):

        json_content = {
            'user_message'          : message,
            'messages_history'      : messages_history,
            # 'user_profile'          : profile,
            # 'explanation_message'   : explanation_message,
            # 'conversational_style'  : self.CONVERSATIONAL_STYLE,
            # 'threshold_met'         : threshold_met,
            # 'program_generation_starting': program_generation_starting
        }
        response_data   = self._call_agent(json_content, 'chat_agent')

        if response_data:
            message = response_data.get('message')
            return message

        return None

    def process_user_message(self, message: str, messages_history: list):
        # self.user_profile                       = self._call_profiler_agent(message, self.user_profile)
        # self.user_profile, explanation_message  = self._call_validator_agent(self.user_profile)
        # self.quality_score                      = self._calculate_quality_score()
        # self.threshold_met                      = self.quality_score >= self.MIN_SCORE_THRESHOLD

        # new_message                               = self._call_chat_agent(message, self.user_profile, explanation_message, self.threshold_met, program_generation_starting)
        new_message                               = self._call_chat_agent(message, messages_history)

        if new_message is None:
            default_fallback_message = "Je suis désolé, je ne comprends pas votre message."
            return default_fallback_message

        return new_message
