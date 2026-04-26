import re

class InputAnalyzer:
    def __init__(self, prompt: str):
        self.prompt = prompt.strip()

    def sanitize(self) -> str:
        """
        Standardizes the input prompt by stripping whitespace and basic cleaning.
        """
        return self.prompt

    def analyze(self) -> dict:
        """
        Analyzes the input prompt and returns metadata.
        """
        return {
            "original_length": len(self.prompt),
            "word_count": len(self.prompt.split()),
            "is_url": bool(re.match(r'https?://[^\s]+', self.prompt)),
            "sanitized_prompt": self.prompt
        }
