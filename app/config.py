from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, computed_field
from typing import Union, List, Optional
from functools import lru_cache
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Settings(BaseSettings):
    # API Settings
    api_base: str = "/api/v1"
    project_name: str = "YtCaptionBridge"
    
    # Environment
    environment: Environment = Environment.PRODUCTION
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    
    # Security
    api_key_name: str = "X-API-Key"
    api_key: str
    
    # Rate Limiting
    rate_limit: str = "60/minute"
    rate_limit_enabled: bool = True
    
    # Cache Settings
    cache_ttl: int = Field(default=3600, ge=0)
    cache_enabled: bool = True
    
    # CORS Settings
    backend_cors_origins: Union[str, List[str]] = ["*"]
    
    # Documentation Settings
    docs_enabled: bool = False
    docs_url: Optional[str] = None
    redoc_url: Optional[str] = None
    
    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    model_config = {
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "protected_namespaces": (),
        "extra": "ignore",
        "frozen": True
    }

    @field_validator("backend_cors_origins")
    @classmethod
    def split_str_to_list(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [i.strip() for i in v.split(",")]
        return v

    @computed_field
    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT

    @field_validator("docs_url", "redoc_url", mode='before')
    def set_docs_urls(cls, v: Optional[str], info) -> Optional[str]:
        if not info.data.get('docs_enabled', False):
            return None
        return "/docs" if info.field_name == "docs_url" else "/redoc"

    @field_validator("log_level", mode='before')
    def set_log_level(cls, v: LogLevel, info) -> LogLevel:
        if info.data.get('environment') == Environment.DEVELOPMENT:
            return LogLevel.DEBUG
        return v

@lru_cache()
def get_settings() -> Settings:
    """Get settings with caching."""
    return Settings()
