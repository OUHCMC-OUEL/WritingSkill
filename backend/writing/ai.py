import json
import re
import google.generativeai as genai
from django.conf import settings


#
def normalize_field(text):
    if not text:
        return ""
    return " ".join(text.split())

#
def extract_json_from_text(text):
    patterns = [
        r'```json\s*(\{.*?\})\s*```',
        r'```\s*(\{.*?\})\s*```',
        r'(\{.*?\})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    return None


def check_grammar(input_text):
    if not isinstance(input_text, str) or not input_text.strip():
        return {
            "result": None,
            "vocabulary": "Input không hợp lệ",
            "grammar": "Input không hợp lệ",
            "coh": "Input không hợp lệ",
            "issues": []
        }

    prompt = f"""You are an English writing improvement system. Analyze the input text and correct grammar, vocabulary, coherence and cohesion errors.

Provide concise explanations in Vietnamese for each type of correction.

Return ONLY a valid JSON object (no markdown, no extra text) in this exact format:
{{
  "result": "Corrected English text in a single paragraph",
  "vocabulary": "Brief Vietnamese explanation of vocabulary issues, combined in one paragraph",
  "grammar": "Brief Vietnamese explanation of grammar issues, combined in one paragraph",
  "coh": "Brief Vietnamese explanation of coherence/cohesion, combined in one paragraph",
  "issues": [
    {{
      "loc": "problematic word or phrase",
      "issue": "type of error",
      "example": "why it was wrong",
      "fix": "suggested correction"
    }}
  ]
}}

Examples:

Input: "He go to school yesterday."
Output: {{"result": "He went to school yesterday.", "vocabulary": "Không có lỗi từ vựng.", "grammar": "Lỗi chia động từ ở thì quá khứ đơn: 'go' phải đổi thành 'went'.", "coh": "Câu văn rõ ràng và mạch lạc.", "issues": [{{"loc": "go", "issue": "wrong verb tense", "example": "used present tense 'go' with past time marker 'yesterday'", "fix": "went"}}]}}

Input: "I am very boring in the class."
Output: {{"result": "I am very bored in the class.", "vocabulary": "Nhầm lẫn giữa 'boring' (gây chán) và 'bored' (cảm thấy chán). Phải dùng 'bored' để diễn tả cảm giác của người.", "grammar": "Sử dụng sai dạng tính từ: 'boring' mô tả đặc điểm của sự vật, 'bored' mô tả cảm xúc của con người.", "coh": "Câu văn rõ ràng và mạch lạc.", "issues": [{{"loc": "boring", "issue": "wrong adjective form", "example": "'boring' describes things that cause boredom, not the feeling itself", "fix": "bored"}}]}}

Now analyze this text:
Input: "{input_text}"

Remember: Return ONLY valid JSON, no markdown formatting."""

    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        result_text = response.text

        # Extract and parse JSON
        data = extract_json_from_text(result_text)

        if not data:
            raise ValueError(f"Could not extract valid JSON. Response: {result_text[:200]}")

        # Normalize and return
        return {
            "result": normalize_field(data.get("result")),
            "vocabulary": normalize_field(data.get("vocabulary")),
            "grammar": normalize_field(data.get("grammar")),
            "coh": normalize_field(data.get("coh")),
            "issues": data.get("issues", [])
        }

    except Exception as e:
        print(f"Grammar check error: {str(e)}")

        return {
            "result": "Lỗi phân tích",
            "vocabulary": "Không thể phân tích do lỗi hệ thống",
            "grammar": "Không thể phân tích do lỗi hệ thống",
            "coh": "Không thể phân tích do lỗi hệ thống",
            "issues": [],
            "error": str(e)
        }