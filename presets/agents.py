from google import genai
from google.genai import types

from presets.instructions import (
    PROFILE_AGENT_SYSTEM_INSTRUCTIONS,
    VALIDATOR_AGENT_SYSTEM_INSTRUCTIONS,
    DURATION_ESTIMATOR_AGENT_SYSTEM_INSTRUCTIONS,
    WORKOUT_ARCHITECT_AGENT_SYSTEM_INSTRUCTIONS,
    NUTRITION_PLANNER_AGENT_SYSTEM_INSTRUCTIONS,
    CHAT_AGENT_SYSTEM_INSTRUCTIONS,
    RE_ENGAGEMENT_AGENT_SYSTEM_INSTRUCTIONS,
    INTENT_RECOGNIZER_SYSTEM_INSTRUCTIONS
)

AGENTS = {
    'profiler_agent': {
        'model'                 : 'gemini-flash-latest',
        'thinking_budget'       : 0,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : PROFILE_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["user_profile"],
                properties = {
                    "user_profile": genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["goal", "sex", "age", "weight", "height", "activity_level", "body_type", "sleep_quality", "stress_level", "illnesses", "allergies", "physical_limitations", "available_equipment", "workout_time_preference", "food_likes", "food_dislikes", "regimes"],
                        properties = {
                            "goal": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "sex": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "age": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "weight": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "height": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "activity_level": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "body_type": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "sleep_quality": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "stress_level": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "illnesses": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "allergies": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "physical_limitations": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "available_equipment": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "workout_time_preference": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "food_likes": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "food_dislikes": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "regimes": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                        },
                    ),
                },
            )
    },
    'validator_agent': {
        'model'                 : 'gemini-flash-latest',
        'thinking_budget'       : -1,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : VALIDATOR_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["user_profile", "explanationMessage"],
            properties = {
                "user_profile": genai.types.Schema(
                    type = genai.types.Type.OBJECT,
                    required = ["goal", "sex", "age", "weight", "height", "activity_level", "body_type", "sleep_quality", "stress_level", "illnesses", "allergies", "physical_limitations", "available_equipment", "workout_time_preference", "food_likes", "food_dislikes", "regimes"],
                    properties = {
                        "goal": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "sex": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "age": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "weight": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "height": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "activity_level": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "body_type": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "sleep_quality": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "stress_level": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "illnesses": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "allergies": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "physical_limitations": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "available_equipment": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "workout_time_preference": genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                        "food_likes": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "food_dislikes": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                        "regimes": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                    },
                ),
                "explanationMessage": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        )
    },
    'duration_estimator_agent': {
        'model'                 : 'gemini-2.5-pro',
        # 'thinking_budget'       : 0,
        'thinking_budget'       : -1,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : DURATION_ESTIMATOR_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["estimated_duration_weeks", "explanation"],
            properties = {
                "estimated_duration_weeks": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                ),
                "explanation": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        )
    },
    'intent_recognizer_agent': {
        'model'                 : 'gemini-flash-latest',
        'thinking_budget'       : 0,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : INTENT_RECOGNIZER_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["demanded_generation", "program_type"],
            properties = {
                "demanded_generation": genai.types.Schema(
                    type = genai.types.Type.BOOLEAN,
                ),
                "program_type": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    enum = ["sport", "nutrition"],
                ),
            },
        )
    },
    'workout_architect_agent': {
        'model'                 : 'gemini-2.5-pro',
        'thinking_budget'       : -1,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : WORKOUT_ARCHITECT_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["program_title", "program_summary", "weekly_schedule"],
            properties = {
                "program_title": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "program_summary": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "weekly_schedule": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["week", "days"],
                        properties = {
                            "week": genai.types.Schema(
                                type = genai.types.Type.NUMBER,
                            ),
                            "days": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.OBJECT,
                                    required = ["title", "exercises"],
                                    properties = {
                                        "title": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "exercises": genai.types.Schema(
                                            type = genai.types.Type.ARRAY,
                                            items = genai.types.Schema(
                                                type = genai.types.Type.OBJECT,
                                                required = ["name", "sets", "reps", "rest", "notes"],
                                                properties = {
                                                    "name": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                    "sets": genai.types.Schema(
                                                        type = genai.types.Type.INTEGER,
                                                    ),
                                                    "reps": genai.types.Schema(
                                                        type = genai.types.Type.INTEGER,
                                                    ),
                                                    "rest": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                    "notes": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                },
                                            ),
                                        ),
                                    },
                                ),
                            ),
                        },
                    ),
                ),
            },
        )
    },
    'nutrition_planner': {
        'model'                 : 'gemini-2.5-pro',
        'thinking_budget'       : -1,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : NUTRITION_PLANNER_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["program_title", "program_summary", "weekly_schedule"],
            properties = {
                "program_title": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "program_summary": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "weekly_schedule": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["week", "days"],
                        properties = {
                            "week": genai.types.Schema(
                                type = genai.types.Type.INTEGER,
                            ),
                            "days": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.OBJECT,
                                    required = ["title", "meals"],
                                    properties = {
                                        "title": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "meals": genai.types.Schema(
                                            type = genai.types.Type.ARRAY,
                                            items = genai.types.Schema(
                                                type = genai.types.Type.OBJECT,
                                                required = ["name", "time", "description"],
                                                properties = {
                                                    "name": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                    "time": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                    "description": genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                },
                                            ),
                                        ),
                                    },
                                ),
                            ),
                        },
                    ),
                ),
            },
        )
    },
    'chat_agent': {
        'model'                 : 'gemini-flash-latest',
        'thinking_budget'       : 0,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : CHAT_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["message"],
            properties = {
                "message": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        )
    },
    're_engagement_agent': {
        'model'                 : 'gemini-2.5-pro',
        'thinking_budget'       : 0,
        'response_mime_type'    : 'application/json',
        'system_instructions'   : RE_ENGAGEMENT_AGENT_SYSTEM_INSTRUCTIONS,
        'genai_response_schema' : genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["notification_message"],
            properties = {
                "notification_message": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        )
    }
}