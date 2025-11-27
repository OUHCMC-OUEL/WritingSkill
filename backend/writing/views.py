from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .ai import check_grammar

class WritingView(viewsets.ViewSet):
    @action(methods=['post'], url_path='check-grammar', detail=False)
    def check_grammar(self, request):
        text = request.data.get("text", "")
        result = check_grammar(text)
        return Response(result, status=status.HTTP_200_OK)

# if __name__ == '__main__':
#     print("GEMINI_API_KEY:", GEMINI_API_KEY)
