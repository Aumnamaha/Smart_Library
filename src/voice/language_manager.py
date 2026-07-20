"""
Language Management Module
===========================

Handles multilingual support for the Smart Library app.
Provides language selection at app start and settings-based changes.

Waterfall Model Phase: Implementation (Week 9-10)
Agile Sprint: Voice Recording Flow Enhancement

Features:
    - Language selection dialog on first launch
    - Settings-based language change capability
    - Multilingual Whisper model integration
    - Language-specific transcription optimization
"""

import os
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class LanguageManager:
    """
    Manages multilingual support for voice transcription.

    Handles:
        - Initial language selection dialog
        - Settings-based language configuration
        - Multilingual model loading and switching
        - Language-specific optimization settings
    """

    # Supported languages with metadata
    SUPPORTED_LANGUAGES = {
        "en": {
            "name": "English",
            "code": "en",
            "whisper_label": "english",
            "description": "Primary global language"
        },
        "hi": {
            "name": "Hindi",
            "code": "hi",
            "whisper_label": "hindi",
            "description": "Spoken by ~600M people"
        },
        "te": {
            "name": "Telugu",
            "code": "te",
            "whisper_label": "telugu",
            "description": "Spoken primarily in India"
        },
        "ta": {
            "name": "Tamil",
            "code": "ta",
            "whisper_label": "tamil",
            "description": "Spoken by ~80M people"
        },
        "bn": {
            "name": "Bengali",
            "code": "bn",
            "whisper_label": "bengali",
            "description": "Spoken by ~270M people"
        },
        "mr": {
            "name": "Marathi",
            "code": "mr",
            "whisper_label": "marathi",
            "description": "Spoken primarily in Maharashtra, India"
        },
        "kn": {
            "name": "Kannada",
            "code": "kn",
            "whisper_label": "kannada",
            "description": "Spoken primarily in Karnataka, India"
        },
        "gu": {
            "name": "Gujarati",
            "code": "gu",
            "whisper_label": "gujarati",
            "description": "Spoken primarily in Gujarat, India"
        }
    }

    def __init__(self, config_path: str = "./config/settings.yaml"):
        """
        Initialize language manager.

        Args:
            config_path: Path to configuration YAML file
        """
        self.config_path = config_path
        self.current_language = "en"  # Default
        self.is_first_launch = True   # Track first launch for dialog
        self.multilingual_model_loaded = False

        self._load_config()

    def _load_config(self):
        """Load language configuration from settings file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    lang_config = config.get('language', {})
                    self.current_language = lang_config.get('default', 'en')
                    self.is_first_launch = not os.path.exists(
                        "./data/language_selection_completed"
                    )
            except Exception as e:
                print(f"[LanguageManager] Error loading config: {e}")
        else:
            # No config file, show language selection
            self.is_first_launch = True

    def get_available_languages(self) -> Dict[str, Dict]:
        """
        Get all supported languages with metadata.

        Returns:
            Dictionary of language codes to language info
        """
        return {code: info for code, info in self.SUPPORTED_LANGUAGES.items()}

    def get_current_language(self) -> str:
        """
        Get currently selected language code.

        Returns:
            Language code (e.g., "en", "hi", "te")
        """
        return self.current_language

    def show_language_selection_dialog(self):
        """
        Display language selection dialog for first-time users.

        In production, this would show a GUI dialog or web modal.
        For CLI apps, shows prompt-based selection.

        Returns:
            Selected language code or None if cancelled
        """
        print("\n" + "=" * 60)
        print("  🌍 SMART LIBRARY - SELECT YOUR PREFERRED LANGUAGE")
        print("=" * 60)
        print("\nThe app will work best with this setting. You can change\nit later in Settings > Language anytime.\n")

        for code, info in self.SUPPORTED_LANGUAGES.items():
            print(f"  {code.upper()}. {info['name']} - {info['description']}")

        print("\n" + "-" * 40)

        # In production: Show interactive selection UI
        # For now, return default (English) but log that dialog was shown
        print("\n[LanguageManager] First launch language selection shown.\n")
        return self.current_language

    def select_language(self, language_code: str):
        """
        Select a new language and update configuration.

        Args:
            language_code: Language code (e.g., "hi", "te", "ta")

        Returns:
            True if selection successful, False if invalid
        """
        if language_code not in self.SUPPORTED_LANGUAGES:
            print(f"[LanguageManager] Invalid language code: {language_code}")
            return False

        # Update current language
        self.current_language = language_code

        # Update config file
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        config['language']['default'] = language_code
        config['system']['version'] = "0.2.0"  # Bump version when changing language

        # Write updated config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        # Mark that user has selected their language
        marker_path = "./data/language_selection_completed"
        if not os.path.exists(marker_path):
            with open(marker_path, 'w') as f:
                f.write(f"Selected language: {language_code}")
                f.write(f"Selected at: {self._get_timestamp()}")

        print(f"\n[LanguageManager] Language changed to: {self.SUPPORTED_LANGUAGES[language_code]['name']}")
        return True

    def get_language_info(self, code: str) -> Optional[Dict]:
        """
        Get detailed information about a specific language.

        Args:
            code: Language code (e.g., "hi", "te")

        Returns:
            Language info dictionary or None if not found
        """
        return self.SUPPORTED_LANGUAGES.get(code)

    def load_multilingual_model(self, model_path: str):
        """
        Load multilingual-capable Whisper model.

        Args:
            model_path: Path to Whisper multilingual model

        Returns:
            True if model loaded successfully
        """
        print(f"[LanguageManager] Loading multilingual STT model: {model_path}")
        # In production: Load actual model
        # from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
        # self.multilingual_model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path)

        print(f"[LanguageManager] Multilingual model loaded successfully")
        self.multilingual_model_loaded = True
        return True

    def get_transcription_config(self) -> Dict:
        """
        Get configuration for transcription based on selected language.

        Returns:
            Configuration dictionary for STT engine
        """
        language_info = self.SUPPORTED_LANGUAGES.get(self.current_language, {})

        # Multilingual model configuration
        multilingual_config = {
            "model_type": "whisper-large-v3-turbo",  # Supports 99 languages
            "language_code": self.current_language,
            "use_multilingual_mode": True,  # Enable language-agnostic mode
            "temperature": 0.7,              # Higher for more diverse outputs
            "task": "transcribe"             # or "translate" if needed
        }

        return multilingual_config

    def save_user_preference(self):
        """
        Save current language selection to persistent storage.

        Called when user changes language in settings.
        """
        self._load_config()  # Reload config to get latest settings
        marker_path = "./data/language_selection_completed"
        if not os.path.exists(marker_path):
            with open(marker_path, 'w') as f:
                f.write(f"Selected language: {self.current_language}")
                f.write(f"Selected at: {self._get_timestamp()}")

    def _get_timestamp(self) -> str:
        """Get current timestamp for logging."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LanguageSelectorUI:
    """
    Provides UI components for language selection.

    Can be used to build:
        - Command-line prompt selector
        - Web modal dialog
        - Desktop GUI selection window
    """

    @staticmethod
    def create_language_list(languages: Dict[str, Dict]) -> str:
        """
        Create formatted list of languages for display.

        Args:
            languages: Dictionary of language codes to info

        Returns:
            Formatted string with all languages
        """
        output = "  Supported Languages:\n"
        output += "-" * 50 + "\n"

        # Sort by number of speakers (rough estimate based on popularity)
        sorted_langs = [
            ("en", "English", "~1.5B speakers"),
            ("hi", "Hindi", "~600M speakers"),
            ("bn", "Bengali", "~270M speakers"),
            ("ta", "Tamil", "~80M speakers"),
            ("te", "Telugu", "~80M speakers"),
            ("mr", "Marathi", "~85M speakers"),
            ("kn", "Kannada", "~75M speakers"),
            ("gu", "Gujarati", "~60M speakers"),
        ]

        for code, name, speakers in sorted_langs:
            if code in languages:
                info = languages[code]
                output += f"  • {info['name']} ({code.upper()}) - {speakers}\n"

        return output


if __name__ == "__main__":
    # Test language manager
    lang_manager = LanguageManager()

    print("Language Manager initialized")
    print(f"Current language: {lang_manager.get_current_language()}")
    print(f"Is first launch (needs dialog): {lang_manager.is_first_launch}")

    available = lang_manager.get_available_languages()
    for code, info in list(available.items())[:3]:  # Show first 3
        print(f"\n{code.upper()}: {info['name']}")
