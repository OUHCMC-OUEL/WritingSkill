#!/bin/bash

python manage.py shell << 'EOF'
from apps.ouel_gemini.models import AIModel, Prompt

ai_model, created = AIModel.objects.get_or_create(
    name="gemini-2.5",
    defaults={
        "provider": "gemini",
        "description": "Gemini 2.5 Flash for grammar correction"
    }
)

# Tạo prompt
prompt = Prompt.objects.create(
    name="grammar_correction",
    version=2,
    purpose="check_grammar",
    instruction="""
    You are an English writing evaluation assistant.
    Your task is to analyze the user's text and return feedback
    in FOUR categories: correctness, clarity, engagement, delivery.
    Respond ONLY in valid JSON.
    """,
    context="""
    Rules:
    - Do not rewrite the entire text
    - Keep original meaning
    - Respond in Vietnamese
    - If no correction or suggestion is needed, set "suggestion": null
    - Do NOT return placeholder text such as "No change needed"
    """,
    settings={
        "temperature": 0.5
    },
    ai_model=ai_model
)

EOF
