"""
DevMind Vector Store
Manages vector storage and retrieval using Pinecone
"""

import asyncio
import json
from typing import List, Dict, Optional, Tuple, Any
from pinecone import Pinecone, ServerlessSpec
import uuid
import time

from .config import config
from .embedding_service import embedding_service

class VectorStore:
    """Vector database interface using Pinecone"""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone connection"""
        try:
            if not config.pinecone_api_key:
                raise ValueError("Pinecone API key not found")
            
            # Initialize Pinecone
            self.pc = Pinecone(api_key=config.pinecone_api_key)
            
            # Create or connect to index
            self._setup_index()
            
            print("✅ Pinecone vector store initialized")
            
        except Exception as e:
            print(f"❌ Pinecone initialization failed: {e}")
            print("🔄 Falling back to local Chroma DB")
            self._initialize_chroma_fallback()
    
    def _setup_index(self):
        """Create or connect to Pinecone index"""
        index_name = config.pinecone_index_name
        
        # Check if index exists
        existing_indexes = self.pc.list_indexes()
        index_exists = any(idx.name == index_name for idx in existing_indexes)
        
        if not index_exists:
            print(f"📝 Creating new Pinecone index: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=config.vector_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            
            # Wait for index to be ready
            time.sleep(10)
        
        # Connect to index
        self.index = self.pc.Index(index_name)
        print(f"✅ Connected to Pinecone index: {index_name}")
    
    def _initialize_chroma_fallback(self):
        """Initialize ChromaDB as fallback"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.chroma_client = chromadb.Client(Settings(
                persist_directory="/app/backend/chroma_db"
            ))
            
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="devmind_codebase"
            )
            
            print("✅ ChromaDB fallback initialized")
            
        except Exception as e:
            print(f"❌ ChromaDB fallback failed: {e}")
    
    async def upsert_code_chunks(
        self, 
        code_chunks: List[Dict[str, Any]]
    ) -> bool:
        """Insert or update code chunks in vector store"""
        
        if self.index:  # Pinecone
            return await self._upsert_pinecone(code_chunks)
        else:  # ChromaDB fallback
            return await self._upsert_chroma(code_chunks)
    
    async def _upsert_pinecone(self, code_chunks: List[Dict[str, Any]]) -> bool:
        """Upsert to Pinecone"""
        try:
            # Generate embeddings
            texts = [chunk["embedding_text"] for chunk in code_chunks]
            embeddings = await embedding_service.generate_embeddings(texts)
            
            # Prepare vectors for upsert
            vectors = []
            for i, chunk in enumerate(code_chunks):
                vector_id = str(uuid.uuid4())
                
                vectors.append({
                    "id": vector_id,
                    "values": embeddings[i],
                    "metadata": {
                        "file_path": chunk["file_path"],
                        "language": chunk["language"],
                        "content": chunk["content"][:1000],  # Truncate for metadata limits
                        "full_content": chunk["content"],
                        "chunk_type": chunk.get("chunk_type", "code")
                    }
                })
            
            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            print(f"✅ Upserted {len(vectors)} code chunks to Pinecone")
            return True
            
        except Exception as e:
            print(f"❌ Pinecone upsert failed: {e}")
            return False
    
    async def _upsert_chroma(self, code_chunks: List[Dict[str, Any]]) -> bool:
        """Upsert to ChromaDB"""
        try:
            texts = [chunk["embedding_text"] for chunk in code_chunks]
            embeddings = await embedding_service.generate_embeddings(
                texts, use_openai=False
            )
            
            ids = [str(uuid.uuid4()) for _ in code_chunks]
            metadatas = [
                {
                    "file_path": chunk["file_path"],
                    "language": chunk["language"],
                    "chunk_type": chunk.get("chunk_type", "code")
                }
                for chunk in code_chunks
            ]
            documents = [chunk["content"] for chunk in code_chunks]
            
            self.chroma_collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            
            print(f"✅ Upserted {len(code_chunks)} code chunks to ChromaDB")
            return True
            
        except Exception as e:
            print(f"❌ ChromaDB upsert failed: {e}")
            return False
    
    async def similarity_search(
        self, 
        query: str, 
        top_k: int = 10,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar code chunks"""
        
        if self.index:  # Pinecone
            return await self._search_pinecone(query, top_k, filter_dict)
        else:  # ChromaDB fallback
            return await self._search_chroma(query, top_k, filter_dict)
    
    async def _search_pinecone(
        self, 
        query: str, 
        top_k: int,
        filter_dict: Optional[Dict]
    ) -> List[Dict[str, Any]]:
        """Search in Pinecone"""
        try:
            # Generate query embedding
            query_embedding = await embedding_service.generate_embeddings([query])
            
            # Search
            results = self.index.query(
                vector=query_embedding[0],
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            return [
                {
                    "content": match.metadata.get("full_content", match.metadata.get("content", "")),
                    "file_path": match.metadata.get("file_path", ""),
                    "language": match.metadata.get("language", ""),
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
            
        except Exception as e:
            print(f"❌ Pinecone search failed: {e}")
            return []
    
    async def _search_chroma(
        self, 
        query: str, 
        top_k: int,
        filter_dict: Optional[Dict]
    ) -> List[Dict[str, Any]]:
        """Search in ChromaDB"""
        try:
            query_embedding = await embedding_service.generate_embeddings(
                [query], use_openai=False
            )
            
            results = self.chroma_collection.query(
                query_embeddings=query_embedding,
                n_results=top_k,
                where=filter_dict
            )
            
            search_results = []
            for i in range(len(results['documents'][0])):
                search_results.append({
                    "content": results['documents'][0][i],
                    "file_path": results['metadatas'][0][i].get("file_path", ""),
                    "language": results['metadatas'][0][i].get("language", ""),
                    "score": 1.0 - results['distances'][0][i],  # Convert distance to similarity
                    "metadata": results['metadatas'][0][i]
                })
            
            return search_results
            
        except Exception as e:
            print(f"❌ ChromaDB search failed: {e}")
            return []
    
    async def delete_by_file_path(self, file_path: str) -> bool:
        """Delete all vectors for a specific file"""
        try:
            if self.index:  # Pinecone
                self.index.delete(filter={"file_path": file_path})
            else:  # ChromaDB
                self.chroma_collection.delete(where={"file_path": file_path})
            
            print(f"✅ Deleted vectors for file: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Delete operation failed: {e}")
            return False

# Global vector store instance
vector_store = VectorStore()