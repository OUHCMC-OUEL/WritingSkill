#!/bin/bash

python manage.py shell << 'EOF'
from apps.ouel_gemini.models import AIModel, Prompt

#ai_model = AIModel.objects.get_or_create(
#    name="gemini-2.5 flash",
#    defaults={
#        "provider": "gemini",
#        "description": "Gemini 2.5 Flash for grammar correction"
#    }
#)

ai_model = AIModel.objects.get(id = 3)

# Tạo prompt
prompt = Prompt.objects.create(
    name="grammar_correction",
    version=3,
    purpose="check-grammar",
    instruction="""
    You are an English writing evaluation assistant.
    Your task is to analyze the user's text and return feedback
    You MUST respond ONLY with valid JSON.
    Do NOT include markdown.
    Do NOT include explanations outside JSON.
    """,
    context="""
    You must return a JSON object with the following top-level fields:
    - "id": a unique string identifier for this evaluation
    - "error": null or a Vietnamese error message if the text cannot be evaluated
    - "correcness"
    - "clarity"
    - "engagement"
    - "delivery"
    For each category (correcness, clarity, engagement, delivery), return an object with:
    - "result":
        • A corrected or improved FULL English sentence (or short paragraph)
        • Keep the original meaning
        • If no improvement is needed, return the original sentence

    - "explanation":
        • Written in Vietnamese
        • Brief explanation or feedback
        • If no issue exists, set this field to None

    - "issues": an array of specific issues
        • If there are no issues, return an empty array []

    Each issue object MUST have:
    - "id": unique string identifier
    - "message": Vietnamese description of the issue
    - "original": the original input text (unchanged)
    - "fix": corrected English text for that specific part
    - "start": starting index of the issue in the original text (integer)
    - "end": ending index of the issue in the original text (integer)
    IMPORTANT RULES:
    - Respond in Vietnamese for all explanations and messages
    - Respond in English ONLY for result and fix
    - Do NOT explain inside result or fix
    - Do NOT rewrite the entire text unless necessary
    - Always return all four categories
    - If the input is NOT English, set "error" and still return all categories with empty issues
    OUTPUT FORMAT:
    {
      "id": "string",
      "original": "string",
      "error": null | "string",

      "correcness": {
        "result": "string",
        "explanation": "string | 'none'",
        "issues": [
          {
            "id": "string",
            "message": "string",
            "original": "string",
            "fix": "string",
            "start": number,
            "end": number
          }
        ]
      },

      "clarity": { same structure },
      "engagement": { same structure },
      "delivery": { same structure }
    }
    """,
    settings={
        "temperature": 0.5
    },
    ai_model=ai_model
)

EOF
