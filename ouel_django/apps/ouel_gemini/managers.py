import time, json
from django.conf import settings
from google import genai
from google.genai import types
from .models import PromptLog, Prompt

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
few_shot_examples = """
Example 1:
Input: "I has finish my homework yesterday."
Output:
{
  "correctness": {
    "review": "Sai thì quá khứ và chia động từ.",
    "suggestion": "I finished my homework yesterday."
  },
  "clarity": {
    "review": "Câu ngắn gọn, dễ hiểu.",
    "suggestion": null
  },
  "engagement": {
    "review": "Câu đơn giản, chưa tạo cảm xúc.",
    "suggestion": "I was happy after finishing my homework yesterday."
  },
  "delivery": {
    "review": "Giọng văn trung tính, phù hợp.",
    "suggestion": null
  }
}

Example 2:
Input: "This essay talk about importance of English in modern world."
Output:
{
  "correctness": {
    "review": "Thiếu mạo từ và chia động từ.",
    "suggestion": "This essay talks about the importance of English in the modern world."
  },
  "clarity": {
    "review": "Ý rõ nhưng thiếu mạo từ làm câu kém tự nhiên.",
    "suggestion": "This essay discusses the importance of English in the modern world."
  },
  "engagement": {
    "review": "Giọng văn học thuật, chưa hấp dẫn.",
    "suggestion": "This essay explores the importance of English in today’s modern world."
  },
  "delivery": {
    "review": "Giọng văn học thuật, phù hợp với bài luận.",
    "suggestion": null
  }
}

Example 3:
Input: "I enjoy learning English because it helps me communicate with people around the world."
Output:
{
  "correctness": {
    "review": "Không có lỗi ngữ pháp hoặc chính tả.",
    "suggestion": null
  },
  "clarity": {
    "review": "Câu rõ ràng, mạch lạc.",
    "suggestion": null
  },
  "engagement": {
    "review": "Câu tự nhiên và tích cực.",
    "suggestion": null
  },
  "delivery": {
    "review": "Giọng văn thân thiện, phù hợp.",
    "suggestion": null
  }
}

Example 4:
Input: "Xin chào bạn"
Output:
{
  "correctness": {
    "review": "Đây không phải là câu tiếng Anh nên không thể đánh giá.",
    "suggestion": null
  },
  "clarity": {
    "review": "Đây không phải là câu tiếng Anh nên không thể đánh giá.",
    "suggestion": null
  },
  "engagement": {
    "review": "Đây không phải là câu tiếng Anh nên không thể đánh giá.",
    "suggestion": null
  },
  "delivery": {
    "review": "Đây không phải là câu tiếng Anh nên không thể đánh giá.",
    "suggestion": null
  }
}
"""
def grammar_correction(input: str, prompt: Prompt):
    start_time = time.time()
    model_settings = {}
    response = ""
    status_code = 200
    token_usage = 0
    error_message = None

    full_instruction = f"{prompt.instruction}\n\nRules: {prompt.context}\nSome examples:\n{few_shot_examples}"

    if prompt.settings:
        model_settings = prompt.settings

    temperature = model_settings.get('temperature', 0.5)

    try:
        response = client.models.generate_content(
            model=prompt.ai_model.name,
            contents=input,
            config=types.GenerateContentConfig(
                system_instruction=full_instruction,
                temperature=temperature,
                response_mime_type="application/json"
            )
        )

        response_text = response.text
        if response.usage_metadata:
            token_usage = response.usage_metadata.total_token_count

        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            status_code = 500
            error_message = "Format trả về bị sai"
            raise ValueError("AI trả về sai định dạng.")
    except Exception as ex:
        status_code = 500
        raise ex
    finally:
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        PromptLog.objects.create(
            prompt=prompt,
            input=input,
            final_context=full_instruction,
            response=response if response else str(error_message),
            token=token_usage,
            latency=latency_ms,
            status=status_code
        )