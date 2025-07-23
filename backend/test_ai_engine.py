"""
DevMind AI Engine Test Script
Test all AI Engine components to ensure proper setup
"""

import asyncio
import json
from ai_engine.config import config
from ai_engine.llm_client import llm_client
from ai_engine.embedding_service import embedding_service
from ai_engine.vector_store import vector_store
from ai_engine.rag_system import rag_system
from ai_engine.agent_framework import agent_framework, AgentTask
from ai_engine.code_processor import code_processor

async def test_config():
    """Test configuration"""
    print("🔧 Testing Configuration...")
    
    if config.validate():
        print("✅ Configuration valid")
        print(f"   - LLM Provider: {config.default_llm_provider}")
        print(f"   - Embedding Model: {config.default_embedding_model}")
        print(f"   - Vector Dimension: {config.vector_dimension}")
    else:
        print("❌ Configuration invalid - check API keys")
    
    print()

async def test_llm_client():
    """Test LLM client"""
    print("🤖 Testing LLM Client...")
    
    try:
        response = await llm_client.generate_response(
            prompt="Write a simple Python function to add two numbers",
            max_tokens=200
        )
        
        if response.content and not response.error:
            print("✅ LLM Client working")
            print(f"   - Provider: {response.provider}")
            print(f"   - Model: {response.model}")
            print(f"   - Response: {response.content[:100]}...")
        else:
            print(f"❌ LLM Client failed: {response.error}")
    
    except Exception as e:
        print(f"❌ LLM Client error: {e}")
    
    print()

async def test_embeddings():
    """Test embedding service"""
    print("🔢 Testing Embedding Service...")
    
    try:
        test_texts = [
            "def add_numbers(a, b): return a + b",
            "function addNumbers(a, b) { return a + b; }",
            "public int addNumbers(int a, int b) { return a + b; }"
        ]
        
        embeddings = await embedding_service.generate_embeddings(test_texts)
        
        if embeddings and len(embeddings) == len(test_texts):
            print("✅ Embedding Service working")
            print(f"   - Generated {len(embeddings)} embeddings")
            print(f"   - Dimension: {len(embeddings[0])}")
        else:
            print("❌ Embedding Service failed")
    
    except Exception as e:
        print(f"❌ Embedding Service error: {e}")
    
    print()

async def test_vector_store():
    """Test vector store"""
    print("📊 Testing Vector Store...")
    
    try:
        # Test data
        test_chunks = [
            {
                "content": "def hello_world(): print('Hello, World!')",
                "language": "python", 
                "file_path": "/test/hello.py",
                "embedding_text": "Python function hello_world in /test/hello.py: def hello_world(): print('Hello, World!')"
            }
        ]
        
        # Test upsert
        success = await vector_store.upsert_code_chunks(test_chunks)
        
        if success:
            print("✅ Vector Store upsert working")
            
            # Test search
            results = await vector_store.similarity_search("python hello world function", top_k=1)
            
            if results:
                print("✅ Vector Store search working")
                print(f"   - Found {len(results)} results")
                print(f"   - Top result score: {results[0]['score']:.3f}")
            else:
                print("❌ Vector Store search failed")
        else:
            print("❌ Vector Store upsert failed")
    
    except Exception as e:
        print(f"❌ Vector Store error: {e}")
    
    print()

async def test_rag_system():
    """Test RAG system"""
    print("🧠 Testing RAG System...")
    
    try:
        # First upsert some test data
        test_chunks = [
            {
                "content": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "language": "python",
                "file_path": "/test/fibonacci.py", 
                "embedding_text": "Python function fibonacci recursive implementation"
            }
        ]
        
        await vector_store.upsert_code_chunks(test_chunks)
        
        # Test query
        result = await rag_system.query_codebase(
            query="How do you implement fibonacci recursively?",
            max_results=1
        )
        
        if result["response"] and not result.get("error"):
            print("✅ RAG System working")
            print(f"   - Found {len(result['relevant_chunks'])} relevant chunks")
            print(f"   - Response: {result['response'][:100]}...")
        else:
            print(f"❌ RAG System failed: {result.get('error')}")
    
    except Exception as e:
        print(f"❌ RAG System error: {e}")
    
    print()

async def test_agent_framework():
    """Test agent framework"""
    print("🤝 Testing Agent Framework...")
    
    try:
        # Start agent framework
        await agent_framework.start()
        
        # Test debug task
        debug_task = AgentTask(
            task_type="debug",
            input_data={
                "code": "print('Hello World'",  # Missing closing parenthesis
                "error_message": "SyntaxError: invalid syntax",
                "language": "python"
            }
        )
        
        task_id = await agent_framework.submit_task(debug_task)
        print(f"✅ Agent Framework working - Task submitted: {task_id}")
        
        # Get agent status
        status = agent_framework.get_agent_status()
        print(f"   - Active agents: {len(status)}")
        
        for agent_name, agent_info in status.items():
            print(f"   - {agent_name}: {agent_info['role']}")
    
    except Exception as e:
        print(f"❌ Agent Framework error: {e}")
    
    print()

def test_code_processor():
    """Test code processor"""
    print("📝 Testing Code Processor...")
    
    try:
        # Test code chunking
        test_code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""
        
        chunks = code_processor._chunk_python_code(test_code, "/test/calc.py")
        
        if chunks:
            print("✅ Code Processor working")
            print(f"   - Generated {len(chunks)} chunks")
            for chunk in chunks:
                print(f"   - {chunk['chunk_type']}: {chunk['name']}")
        else:
            print("❌ Code Processor failed")
    
    except Exception as e:
        print(f"❌ Code Processor error: {e}")
    
    print()

async def run_all_tests():
    """Run all tests"""
    print("🚀 DevMind AI Engine Test Suite")
    print("=" * 50)
    
    await test_config()
    await test_llm_client()
    await test_embeddings()
    await test_vector_store()
    await test_rag_system()
    await test_agent_framework()
    test_code_processor()
    
    print("🏁 Test Suite Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_all_tests())