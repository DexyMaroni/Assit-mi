from django.core.management.base import BaseCommand
from core.gemini_utils import generate_content

class Command(BaseCommand):
    help = "Test Gemini API integration"

    def handle(self, *args, **kwargs):
        # Test prompt
        prompt = "Explain how AI works"
        result = generate_content(prompt)
        self.stdout.write(self.style.SUCCESS(f"Generated Content: {result}"))
