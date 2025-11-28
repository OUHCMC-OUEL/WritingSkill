import os
import json
import genai

def normalize_field(text):
    if not text:
        return ""
    return " ".join(text.split())

def check_grammar(input_text):
    if not isinstance(input_text, str) or not input_text.strip():
        return {
            "output": None,
            "vocabulary": "Input không hợp lệ",
            "grammar": "Input không hợp lệ",
            "coherence": "Input không hợp lệ",
            "issues": []
        }

    prompt = f"""
You are a system that improves English writing skills. Correct grammar, vocabulary, coherence and cohesion. Provide concise explanations for each correction in Vietnamese.

Return ONLY JSON in the following format:
{{
    "output": "Corrected English sentence or paragraph (single paragraph).",
    "vocabulary": "Short explanation in Vietnamese about vocabulary issues, gộp thành một đoạn duy nhất.",
    "grammar": "Short explanation in Vietnamese about grammar issues, gộp thành một đoạn duy nhất.",
    "coherence": "Short explanation in Vietnamese about coherence/cohesion, gộp thành một đoạn duy nhất.",
    "issues": [
        {{
            "loc": "word or phrase",
            "issue": "type of error",
            "example": "how it was wrong",
            "fix": "suggested fix"
        }}
    ]
}}

Few-shot examples:

Input: "He go to school yesterday."
Output:
{{
    "output": "He went to school yesterday.",
    "vocabulary": "Không có lỗi sai từ vựng",
    "grammar": "Lỗi thì động từ, đã sửa sang quá khứ",
    "coherence": "Câu rõ ràng, mạch lạc",
    "issues": [
        {{"loc": "go", "issue": "wrong tense", "example": "go → should be past", "fix": "went"}}
    ]
}}

Input: "I am very boring in the class."
Output:
{{
    "output": "I am very bored in the class.",
    "vocabulary": "Sai tính từ, dùng bored thay vì boring",
    "grammar": "Sai dạng tính từ mô tả cảm giác, đã sửa",
    "coherence": "Câu rõ ràng, mạch lạc",
    "issues": [
        {{"loc": "boring", "issue": "wrong adjective for feeling", "example": "boring → describes object, not feeling", "fix": "bored"}}
    ]
}}

Now process:
Input: "{input_text}"
"""

    # Gọi Gemini API
    from google import genai
    from django.conf import settings

    GEMINI_API_KEY = settings.GEMINI_API_KEY
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )

    result_text = response.text

    try:
        start = result_text.find("{")
        end = result_text.rfind("}") + 1
        json_str = result_text[start:end]
        data = json.loads(json_str)

        result = {
            "output": normalize_field(data.get("output")),
            "vocabulary": normalize_field(data.get("vocabulary")),
            "grammar": normalize_field(data.get("grammar")),
            "coherence": normalize_field(data.get("coherence")),
            "issues": data.get("issues", [])
        }
        return result

    except Exception as e:
        return {
            "output": None,
            "vocabulary": "Lỗi phân tích JSON",
            "grammar": "Lỗi phân tích JSON",
            "coherence": "Lỗi phân tích JSON",
            "issues": [],
            "raw_output": result_text,
            "error": str(e)
        }
