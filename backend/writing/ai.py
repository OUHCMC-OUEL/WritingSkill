import json
import re

from google import genai
from django.conf import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
def parse_gemini_json(text):
    text_clean = re.sub(r"^```(?:json)?\n", "", text)
    text_clean = re.sub(r"```$", "", text_clean.strip())
    try:
        return json.loads(text_clean)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from Gemini", "raw": text}

def check_grammar(text):
    prompt = f"""
    Task: Correct the English sentence and provide concise feedback.
    - Return JSON ONLY, no extra text.
    - If not English, return:
    {{
      "correct_text": null,
      "vocabulary": "Not English",
      "grammar": "Not English",
      "coh": "Not English",
      "issues": []
    }}

    - If English, provide:
      1. "correct_text": corrected sentence.
      2. "vocabulary": short note on vocabulary issues.
      3. "grammar": short note on grammar issues.
      4. "coh": short note on coherence/cohesion.
      5. "issues": list of detailed corrections:
          - loc: the word or phrase
          - issue: what type of error it is
          - example: how it was wrong
          - fix: suggested fix

    FEW-SHOT EXAMPLES:

    Input: "He go to school yesterday."
    Output:
    {{
      "correct_text": "He went to school yesterday.",
      "vocabulary": "OK",
      "grammar": "Verb tense error",
      "coh": "Clear",
      "issues": [
        {{"loc": "go", "issue": "wrong tense", "example": "go → should be past", "fix": "went"}}
      ]
    }}

    Input: "I am very boring in the class."
    Output:
    {{
      "correct_text": "I am very bored in the class.",
      "vocabulary": "Wrong adjective",
      "grammar": "Participle/adjective choice",
      "coh": "Clear",
      "issues": [
        {{"loc": "boring", "issue": "wrong adjective for feeling", "example": "boring → describes object, not feeling", "fix": "bored"}}
      ]
    }}

    NOW PROCESS:
    Input: "{text}"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )
    result_dict = parse_gemini_json(response.text)
    return result_dict

if __name__ == "__main__":
    print(check_grammar("Yesterday I go to the market and buy many fruit. The weather was very hot so I don’t feels good. My friend tell me he will meets me there but he never come. I was wait for him for two hour before I leaving. It make me very annoying."))