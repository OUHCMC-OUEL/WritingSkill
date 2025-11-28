import os
import json
import genai
from django.conf import settings

def normalize_field(text):
    if not text:
        return ""
    return " ".join(text.split())

def check_grammar(input_text):
    if not isinstance(input_text, str) or not input_text.strip():
        return {
            "result": None,
            "vocabulary": "Input không hợp lệ",
            "grammar": "Input không hợp lệ",
            "coh": "Input không hợp lệ",
            "issues": []
        }

    prompt = f"""
You are a system that improves English writing skills. Correct grammar, vocabulary, coherence and cohesion. Provide concise explanations for each correction in Vietnamese.

Return ONLY JSON in the following format:
{{
    "result": "Corrected English sentence or paragraph (single paragraph).",
    "vocabulary": "Short explanation in Vietnamese about vocabulary issues, gộp thành một đoạn duy nhất.",
    "grammar": "Short explanation in Vietnamese about grammar issues, gộp thành một đoạn duy nhất.",
    "coh": "Short explanation in Vietnamese about coherence/cohesion, gộp thành một đoạn duy nhất.",
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
    "result": "He went to school yesterday.",
    "vocabulary": "Không có lỗi sai từ vựng",
    "grammar": "Lỗi thì động từ, đã sửa sang quá khứ",
    "coh": "Câu rõ ràng, mạch lạc",
    "issues": [
        {{"loc": "go", "issue": "wrong tense", "example": "go → should be past", "fix": "went"}}
    ]
}}

Input: "I am very boring in the class."
Output:
{{
    "result": "I am very bored in the class.",
    "vocabulary": "Sai tính từ, dùng bored thay vì boring",
    "grammar": "Sai dạng tính từ mô tả cảm giác, đã sửa",
    "coh": "Câu rõ ràng, mạch lạc",
    "issues": [
        {{"loc": "boring", "issue": "wrong adjective for feeling", "example": "boring → describes object, not feeling", "fix": "bored"}}
    ]
}}

Now process:
Input: "{input_text}"
"""

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )

    result_text = response.text

    try:
        # Extract JSON only
        start = result_text.find("{")
        end = result_text.rfind("}") + 1
        json_str = result_text[start:end]

        data = json.loads(json_str)

        return {
            "result": normalize_field(data.get("result")),
            "vocabulary": normalize_field(data.get("vocabulary")),
            "grammar": normalize_field(data.get("grammar")),
            "coh": normalize_field(data.get("coh")),
            "issues": data.get("issues", [])
        }

    except Exception as e:
        return {
            "result": "Lỗi phân tích",
            "vocabulary": "Lỗi phân tích",
            "grammar": "Lỗi phân tích",
            "coh": "Lỗi phân tích",
            "issues": [],
            "error": str(e)
        }
