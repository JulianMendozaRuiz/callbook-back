import os
from typing import Optional

import assemblyai as aai
import requests
from dotenv import load_dotenv

load_dotenv()

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY", "your_assemblyai_api_key")


class AssemblyAIService:
    """Singleton service for AssemblyAI API operations"""

    _instance: Optional["AssemblyAIService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize(self):
        """Initialize the AssemblyAI settings"""
        # Configure the API key for regular transcription
        aai.settings.api_key = ASSEMBLYAI_API_KEY

    def generate_realtime_token(self, expires_in_seconds: int = 600) -> str:
        """
        Generate a temporary token for real-time transcription using direct API call

        Args:
            expires_in_seconds: Token expiration time in seconds (max: 600 seconds / 10 minutes)

        Returns:
            str: Temporary token for client-side use
        """
        try:
            # Ensure expires_in_seconds is within the allowed range (1-600 seconds)
            expires_in_seconds = max(1, min(expires_in_seconds, 600))

            # Make direct API call to generate token
            url = "https://streaming.assemblyai.com/v3/token"
            headers = {"Authorization": ASSEMBLYAI_API_KEY}
            params = {"expires_in_seconds": expires_in_seconds}

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            token_data = response.json()
            return token_data.get("token", "")

        except Exception as e:
            raise Exception(f"Failed to generate AssemblyAI token: {str(e)}")


# Global singleton instance
assemblyai_service = AssemblyAIService()
