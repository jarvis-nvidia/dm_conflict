"""
DevMind LLM Client
Unified interface for multiple LLM providers (Together AI, Groq, OpenAI)
"""

import asyncio
import json
from typing import Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass
import httpx
from groq import Groq
import openai
from together import Together

from .config import config

@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    usage: Optional[Dict] = None
    error: Optional[str] = None

class LLMClient:
    """Unified LLM client with fallback support"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available LLM providers"""
        try:
            # Together AI
            if config.together_api_key:
                self.providers['together'] = Together(api_key=config.together_api_key)
                print("✅ Together AI initialized")
        except Exception as e:
            print(f"❌ Together AI initialization failed: {e}")
        
        try:
            # Groq
            if config.groq_api_key:
                self.providers['groq'] = Groq(api_key=config.groq_api_key)
                print("✅ Groq initialized")
        except Exception as e:
            print(f"❌ Groq initialization failed: {e}")
        
        try:
            # OpenAI
            if config.openai_api_key:
                openai.api_key = config.openai_api_key
                self.providers['openai'] = openai
                print("✅ OpenAI initialized")
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
    
    async def generate_response(
        self, 
        prompt: str, 
        provider: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate response with fallback mechanism"""
        
        provider = provider or config.default_llm_provider
        
        # Try primary provider
        try:
            return await self._call_provider(
                provider, prompt, max_tokens, temperature, system_prompt
            )
        except Exception as e:
            print(f"❌ Primary provider {provider} failed: {e}")
        
        # Fallback to other providers
        for fallback_provider in self.providers.keys():
            if fallback_provider != provider:
                try:
                    print(f"🔄 Trying fallback provider: {fallback_provider}")
                    return await self._call_provider(
                        fallback_provider, prompt, max_tokens, temperature, system_prompt
                    )
                except Exception as e:
                    print(f"❌ Fallback provider {fallback_provider} failed: {e}")
                    continue
        
        return LLMResponse(
            content="", 
            model="none", 
            provider="none",
            error="All LLM providers failed"
        )
    
    async def _call_provider(
        self, 
        provider: str, 
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str]
    ) -> LLMResponse:
        """Call specific LLM provider"""
        
        if provider == "together":
            return await self._call_together(prompt, max_tokens, temperature, system_prompt)
        elif provider == "groq":
            return await self._call_groq(prompt, max_tokens, temperature, system_prompt)
        elif provider == "openai":
            return await self._call_openai(prompt, max_tokens, temperature, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    async def _call_together(self, prompt: str, max_tokens: int, temperature: float, system_prompt: Optional[str]) -> LLMResponse:
        """Call Together AI API"""
        client = self.providers['together']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=config.llm_models["together"]["model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=config.llm_models["together"]["model"],
            provider="together",
            usage=response.usage.__dict__ if hasattr(response, 'usage') else None
        )
    
    async def _call_groq(self, prompt: str, max_tokens: int, temperature: float, system_prompt: Optional[str]) -> LLMResponse:
        """Call Groq API"""
        client = self.providers['groq']
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=config.llm_models["groq"]["model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=config.llm_models["groq"]["model"],
            provider="groq",
            usage=response.usage.__dict__ if hasattr(response, 'usage') else None
        )
    
    async def _call_openai(self, prompt: str, max_tokens: int, temperature: float, system_prompt: Optional[str]) -> LLMResponse:
        """Call OpenAI API"""
        client = openai.OpenAI(api_key=config.openai_api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=config.llm_models["openai"]["model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=config.llm_models["openai"]["model"],
            provider="openai",
            usage=response.usage.__dict__ if hasattr(response, 'usage') else None
        )

# Global LLM client instance
llm_client = LLMClient()