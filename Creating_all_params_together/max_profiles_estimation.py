import json
from tiktoken import get_encoding
from prompt_builder import prompt 
from schema import StudentParameters

enc = get_encoding("gpt2")

# Render prompt without any memory_block to get the static overhead
static_prompt = prompt.format(memory_block="")
static_tokens = len(enc.encode(static_prompt))

from schema import StudentParameters

sample_profile = StudentParameters(
    conceptual_clarity_level=3,
    attention_span_category=2,
    retention_strength=65.0,
    problem_solving_speed_sec=240,
    error_pattern="calculation",
    growth_slope=0.2,

    response_to_feedback=4,
    revisions_per_week=2,
    days_between_revisions=3,
    method_of_revision=["active_recall", "spaced_repetition"],
    question_asking_nature=2,
    self_assessment_accuracy=-10.0,
    exploration_tendency=3,

    teacher_relationship_quality=4,
    peer_learning_behavior=2,
    communication_clarity=3,
    discussion_engagement=3,

    test_anxiety_level=3,
    resilience_after_failure=3,
    motivation_intrinsic_vs_extrinsic=0.6,
    achievement_orientation=2,
    emotional_self_awareness=3,

    device_access_type=2,
    preferred_edtech_apps=["khan", "quizlet", "desmos"],
    digital_distraction_level=3,
    input_method_preference="typing",

    highest_academic_level="high_school",
    study_space_quality=4,
    academic_pressure_at_home=3,
    family_responsibilities_hrs=2,
    support_system_strength=2,

    content_type_preference=["video", "practice_tests"],

    # must be the exact prefix of ALLOWED_KG_NODES up through "Uniform Linear Motion"
    knowledge_graph_nodes_covered=[
        "Sundial",
        "Water Clock",
        "Hourglass",
        "Candle Clock",
        "Simple Pendulum",
        "Time Period of Pendulum",
        "Speed",
        "SI Unit of Time",
        "Uniform Linear Motion"
    ],
    ongoing_concept="Non-uniform Linear Motion",

    metacognitive_skill_level=3,

    next_section="Details (facts, sub-concepts)",
    difficulty=3,
    board_exam_importance=4,
    olympiad_importance=2,
    avg_study_time_min=3,
    interest_evoking=3,
    curiosity_evoking=4,
    critical_reasoning_needed=3,
    inquiry_learning_scope=4,
    example_availability=4
).model_dump()


profile_json = json.dumps(sample_profile,indent=2)

# Count tokens for one profile entry plus the comma that separates list items
profile_tokens = len(enc.encode(profile_json)) + len(enc.encode(","))

MAX_CONTEXT = 1_000_000
available_for_profiles = MAX_CONTEXT - static_tokens

max_profiles = available_for_profiles // profile_tokens
print(f"Static tokens: {static_tokens}")
print(f"Tokens per profile: {profile_tokens}")
print(f"Estimated max profiles: {max_profiles}")
