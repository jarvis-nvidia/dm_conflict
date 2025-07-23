"""
DevMind Embedding Service
Handles code chunk embedding generation for semantic search
"""

import asyncio
import numpy as np
from typing import List, Dict, Optional, Tuple
import openai
from sentence_transformers import SentenceTransformer
import tiktoken

from .config import config

class EmbeddingService:
    """Service for generating embeddings from code chunks"""
    
    def __init__(self):
        self.openai_client = None
        self.sentence_transformer = None
        self.tokenizer = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize embedding services"""
        try:
            # OpenAI embeddings (primary)
            if config.openai_api_key:
                self.openai_client = openai.OpenAI(api_key=config.openai_api_key)
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
                print("✅ OpenAI embeddings initialized")
        except Exception as e:
            print(f"❌ OpenAI embeddings initialization failed: {e}")
        
        try:
            # Sentence transformers (fallback)
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Sentence Transformers initialized")
        except Exception as e:
            print(f"❌ Sentence Transformers initialization failed: {e}")
    
    async def generate_embeddings(
        self, 
        texts: List[str], 
        use_openai: bool = True
    ) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        
        if use_openai and self.openai_client:
            try:
                return await self._generate_openai_embeddings(texts)
            except Exception as e:
                print(f"❌ OpenAI embeddings failed: {e}")
                print("🔄 Falling back to Sentence Transformers")
        
        # Fallback to sentence transformers
        return await self._generate_sentence_embeddings(texts)
    
    async def _generate_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        # Chunk texts to avoid token limits
        chunked_texts = self._chunk_texts_for_embedding(texts)
        all_embeddings = []
        
        for chunk in chunked_texts:
            response = self.openai_client.embeddings.create(
                model=config.default_embedding_model,
                input=chunk
            )
            
            embeddings = [data.embedding for data in response.data]
            all_embeddings.extend(embeddings)
        
        return all_embeddings
    
    async def _generate_sentence_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Sentence Transformers"""
        def encode_texts():
            return self.sentence_transformer.encode(texts, convert_to_tensor=False)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, encode_texts)
        
        return embeddings.tolist()
    
    def _chunk_texts_for_embedding(self, texts: List[str], max_tokens: int = 8000) -> List[List[str]]:
        """Chunk texts to fit within token limits"""
        if not self.tokenizer:
            # If no tokenizer, use simple chunking
            return [texts[i:i+10] for i in range(0, len(texts), 10)]
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for text in texts:
            text_tokens = len(self.tokenizer.encode(text))
            
            if current_tokens + text_tokens > max_tokens and current_chunk:
                chunks.append(current_chunk)
                current_chunk = [text]
                current_tokens = text_tokens
            else:
                current_chunk.append(text)
                current_tokens += text_tokens
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def prepare_code_for_embedding(self, code: str, language: str, file_path: str) -> Dict[str, str]:
        """Prepare code chunk with metadata for embedding"""
        return {
            "content": code,
            "language": language,
            "file_path": file_path,
            "embedding_text": f"Language: {language}\nFile: {file_path}\nCode:\n{code}"
        }

# Global embedding service instance
embedding_service = EmbeddingService()