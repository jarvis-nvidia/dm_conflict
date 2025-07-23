"""
DevMind AI Engine Configuration
Centralized configuration management for all AI components
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AIConfig:
    """AI Engine Configuration"""
    
    # API Keys
    together_api_key: str = os.getenv("TOGETHER_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Model Configuration
    default_llm_provider: str = os.getenv("DEFAULT_LLM_PROVIDER", "together")
    default_embedding_model: str = os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-3-small")
    vector_dimension: int = int(os.getenv("VECTOR_DIMENSION", "1536"))
    max_context_length: int = int(os.getenv("MAX_CONTEXT_LENGTH", "4000"))
    
    # Vector Store Configuration
    pinecone_index_name: str = "devmind-codebase"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # LLM Provider Configuration
    llm_models: Dict[str, Dict[str, str]] = None
    
    def __post_init__(self):
        self.llm_models = {
            "together": {
                "model": "meta-llama/Llama-2-7b-chat-hf",  # Use smaller available model
                "api_key": self.together_api_key
            },
            "groq": {
                "model": "llama3-8b-8192",  # Use available model
                "api_key": self.groq_api_key
            },
            "openai": {
                "model": "gpt-3.5-turbo",
                "api_key": self.openai_api_key
            }
        }
    
    def validate(self) -> bool:
        """Validate that required API keys are present"""
        required_keys = [
            self.together_api_key or self.groq_api_key,
            self.openai_api_key,
            self.pinecone_api_key
        ]
        return all(bool(key) for key in required_keys)

# Global configuration instance
config = AIConfig()

# Validate configuration on import
if not config.validate():
    print("⚠️  Warning: Some required API keys are missing!")
    print("Please check your .env file configuration.")