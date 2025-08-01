import json
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

load_dotenv()

GOOGLE_CLOUD_CREDENTIALS = os.environ.get("GOOGLE_CLOUD_CREDENTIALS", "{}")


class GoogleTranslateService:
    """Singleton service for Google Cloud Translate API operations"""

    _instance: Optional["GoogleTranslateService"] = None
    _client: Optional[translate.Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize(self):
        """Initialize the Google Translate client"""
        if self._client is None:
            try:
                # Parse credentials from environment variable
                credentials_info = json.loads(GOOGLE_CLOUD_CREDENTIALS)

                # Create credentials object from the JSON
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info
                )

                # Initialize the client with credentials
                self._client = translate.Client(credentials=credentials)

            except json.JSONDecodeError:
                raise ValueError(
                    "Invalid GOOGLE_CLOUD_CREDENTIALS format. Must be valid JSON."
                )
            except Exception as e:
                raise Exception(
                    f"Failed to initialize Google Translate client: {str(e)}"
                )

    @property
    def client(self) -> translate.Client:
        """
        Get the Google Translate client instance.

        This property lazily initializes the client if it has not been created yet.
        """
        if self._client is None:
            self._initialize()
        if self._client is None:
            raise RuntimeError("Google Translate client could not be initialized.")
        return self._client

    def translate_text(
        self,
        text: str,
        target_language: str = "en",
        source_language: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Translate text to target language

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Source language code (optional, auto-detected if None)

        Returns:
            Dict containing translated text and metadata
        """
        try:
            result = self.client.translate(
                text, target_language=target_language, source_language=source_language
            )

            return {
                "translatedText": result["translatedText"],
                "detectedSourceLanguage": result.get("detectedSourceLanguage"),
                "input": text,
                "targetLanguage": target_language,
            }

        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")


# Global singleton instance
google_translate_service = GoogleTranslateService()
