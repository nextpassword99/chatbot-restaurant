from app.core.config import settings
import subprocess


class Gemma2:
    async def load_model(self):
        return self

    async def handle_text(self, msg):
        result = subprocess.run(f"ollama run {settings.MODEL_GEMMA} {msg}",
                                shell=True,
                                capture_output=True)

        return result.stdout.decode("utf-8")

    @classmethod
    def justResponse(self, response):
        return response
