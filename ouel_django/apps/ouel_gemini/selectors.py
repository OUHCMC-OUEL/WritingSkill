from .models import Prompt

def get_grammar_prompt(purpose: str) -> Prompt:
    prompt = Prompt.objects.filter(purpose=purpose, active=True).order_by('-version').first()
    if prompt:
        return prompt

    raise ValueError(f"Không tìm thấy Prompt phù hợp cho model: {purpose}")
