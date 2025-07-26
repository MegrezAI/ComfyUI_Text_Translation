"""
Bing/Azure Text Translation implementation using Azure SDK
This module provides a clean interface for Azure Text Translation service
"""

import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text.models import InputTextItem
from dotenv import load_dotenv

from azure.core.exceptions import HttpResponseError

load_dotenv()
# Read Azure translation service configuration from environment variables
AZURE_TRANSLATOR_CONFIG = {
    'api_key': os.getenv('AZURE_TRANSLATOR_API_KEY', ''),
    'region': os.getenv('AZURE_TRANSLATOR_REGION', 'eastasia'),
    'endpoint': os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')
}


class BingTranslator:
    """Azure Text Translation client wrapper"""
    
    def __init__(self):
        """Initialize Azure Text Translation client with config from environment variables"""
        config = AZURE_TRANSLATOR_CONFIG
        
        # Validate required configuration
        if not config['api_key']:
            raise ValueError("AZURE_TRANSLATOR_API_KEY environment variable is required")
        
        self.api_key = config['api_key']
        self.region = config['region']
        self.endpoint = config['endpoint']
        
        # Create client
        credential = AzureKeyCredential(self.api_key)
        self.client = TextTranslationClient(endpoint=self.endpoint, credential=credential, region=self.region)
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., "en", "zh", "ja")
            source_language: Source language code (default: "auto" for auto-detection)
        
        Returns:
            Translated text
        """
        if not text:
            return ""
        
        try:
            # Prepare input
            input_text_elements = [InputTextItem(text=text)]
            
            # Handle auto-detect source language
            from_language = None if source_language == "auto" else source_language
            
            # Translate
            response = self.client.translate(
                body=input_text_elements,
                to_language=[target_language],
                from_language=from_language
            )
            
            if response and response[0] and response[0].translations:
                return response[0].translations[0].text
            else:
                return ""
                
        except HttpResponseError as exception:
            if exception.error is not None:
                raise Exception(f"Azure Translation Error: {exception.error.code} - {exception.error.message}")
            raise Exception(f"Azure Translation Error: {str(exception)}")
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def detect_language(self, text: str) -> dict:
        """
        Detect the language of the input text
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with language code and confidence score
        """
        if not text:
            return {"language": "", "score": 0.0}
        
        try:
            input_text_elements = [InputTextItem(text=text)]
            
            # Translate to English to get language detection
            response = self.client.translate(
                body=input_text_elements,
                to_language=["en"]
            )
            
            if response and response[0] and response[0].detected_language:
                detected = response[0].detected_language
                return {
                    "language": detected.language,
                    "score": detected.score
                }
            else:
                return {"language": "", "score": 0.0}
                
        except Exception as e:
            raise Exception(f"Language detection failed: {str(e)}")
    
    def get_supported_languages(self) -> dict:
        """
        Get list of supported languages
        
        Returns:
            Dictionary with supported languages information
        """
        try:
            response = self.client.get_supported_languages()
            
            result = {
                "translation": {},
                "transliteration": {},
                "dictionary": {}
            }
            
            if response.translation is not None:
                for key, value in response.translation.items():
                    result["translation"][key] = {
                        "name": value.name,
                        "native_name": value.native_name
                    }
            
            if response.transliteration is not None:
                for key, value in response.transliteration.items():
                    result["transliteration"][key] = {
                        "name": value.name,
                        "scripts": len(value.scripts) if hasattr(value, 'scripts') else 0
                    }
            
            if response.dictionary is not None:
                for key, value in response.dictionary.items():
                    result["dictionary"][key] = {
                        "name": value.name,
                        "target_languages": len(value.translations) if hasattr(value, 'translations') else 0
                    }
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to get supported languages: {str(e)}")


def create_bing_translator() -> BingTranslator:
    """
    Factory function to create a BingTranslator instance with config from environment variables
    
    Environment variables required:
    - AZURE_TRANSLATOR_API_KEY: Azure translation service API key
    
    Optional environment variables:
    - AZURE_TRANSLATOR_REGION: Azure region (default: eastasia)
    - AZURE_TRANSLATOR_ENDPOINT: Translation service endpoint (default: https://api.cognitive.microsofttranslator.com)
    
    Returns:
        BingTranslator instance
    """
    return BingTranslator()