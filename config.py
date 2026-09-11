"""Configuration management using Pydantic and YAML."""
import os
from typing import Dict, List, Optional, Literal
from pathlib import Path
from pydantic import BaseModel, Field, validator
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class APIConfig(BaseModel):
    """API Configuration."""
    openai_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    elevenlabs_key: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))
    elevenlabs_voice_id: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_VOICE_ID", ""))

    @validator('openai_key', 'elevenlabs_key', 'elevenlabs_voice_id')
    def validate_keys(cls, v):
        if not v or v == "":
            raise ValueError("API key is required")
        return v

    class Config:
        case_sensitive = False


class OpenAIConfig(BaseModel):
    """OpenAI API settings."""
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2000
    response_format: str = "json_object"


class VoiceConfig(BaseModel):
    """ElevenLabs voice settings."""
    model_id: str = "eleven_multilingual_v2"
    stability: float = 0.35
    similarity_boost: float = 0.85
    enable_logging: bool = False


class AvatarConfig(BaseModel):
    """Avatar display configuration."""
    height: int = 380
    position: List[str] = ["right", "bottom"]
    audio_reactivity: Dict = Field(
        default_factory=lambda: {
            "enabled": True,
            "min_volume_threshold": 0.15,
            "max_scale_factor": 1.08
        }
    )


class VideoConfig(BaseModel):
    """Video processing settings."""
    output_resolution: List[int] = [1280, 720]
    fps: int = 24
    codec: str = "libx264"
    preset: Literal["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"] = "medium"
    audio_bitrate: str = "192k"
    video_bitrate: str = "5000k"
    output_filename: str = "AUTOMATED_YOUTUBE_OUTPUT.mp4"


class FileConfig(BaseModel):
    """File management settings."""
    temp_directory: str = ".temp"
    cleanup_on_exit: bool = True
    verbose_logging: bool = False


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    log_file: str = "logs/automation.log"
    console_output: bool = True
    max_log_size_mb: int = 10
    backup_count: int = 3


class ScriptConfig(BaseModel):
    """Script generation settings."""
    enable_timestamp_validation: bool = True
    default_scene_duration: float = 5.0
    min_scene_duration: float = 1.0
    max_scene_duration: float = 30.0


class AppConfig(BaseModel):
    """Root application configuration."""
    api: APIConfig
    openai: OpenAIConfig
    voice: VoiceConfig
    sprites: Dict[str, str]
    avatar: AvatarConfig
    video: VideoConfig
    files: FileConfig
    logging: LoggingConfig
    script: ScriptConfig

    class Config:
        case_sensitive = False


def load_config(config_path: str = "config.yaml") -> AppConfig:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to the config.yaml file
        
    Returns:
        AppConfig instance with all settings
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If required keys are missing
    """
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    if not config_dict:
        raise ValueError("Config file is empty")
    
    return AppConfig(**config_dict)


def validate_config(config: AppConfig) -> bool:
    """Validate that all required configuration is present.
    
    Args:
        config: AppConfig instance to validate
        
    Returns:
        True if valid, raises exception otherwise
    """
    # Check API keys
    if not config.api.openai_key:
        raise ValueError("OPENAI_API_KEY not configured")
    if not config.api.elevenlabs_key:
        raise ValueError("ELEVENLABS_API_KEY not configured")
    if not config.api.elevenlabs_voice_id:
        raise ValueError("ELEVENLABS_VOICE_ID not configured")
    
    # Check sprite files exist
    for emotion, sprite_path in config.sprites.items():
        if not Path(sprite_path).exists():
            raise FileNotFoundError(f"Sprite file missing for '{emotion}': {sprite_path}")
    
    # Check video resolution
    if len(config.video.output_resolution) != 2:
        raise ValueError("Video resolution must be [width, height]")
    
    return True


# Global config instance (lazy loaded)
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance (lazy loads on first access).
    
    Returns:
        AppConfig instance
    """
    global _config
    if _config is None:
        _config = load_config()
        validate_config(_config)
    return _config
