"""
Initialize the RAGmail vector database
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.document_loader import RAGmailDocumentLoader
from src.vector_store import RAGmailVectorStore

def main():
    print("=" * 80)
    print("RAGmail Vector Database Initialization")
    print("=" * 80)
    print()
    
    # Load documents
    print("Step 1: Loading documents...")
    loader = RAGmailDocumentLoader()
    documents = loader.load_all_documents()
    print(f"✓ Loaded {len(documents)} documents")
    print()
    
    # Create vector store
    print("Step 2: Creating vector database...")
    print("  - Downloading embedding model (first time only)...")
    print("  - Generating embeddings for all documents...")
    print("  - This may take 2-3 minutes...")
    print()
    
    vector_store = RAGmailVectorStore()
    vector_store.create_vectorstore(documents)
    
    print()
    print("=" * 80)
    print("✓ Vector Database Successfully Created!")
    print("=" * 80)
    print()
    print("Next step: Run 'python main.py' to start generating emails!")
    print()
    
    # Test search
    print("Quick test - searching for 'multi-agent systems'...")
    results = vector_store.search_projects_only("multi-agent systems and LangGraph", k=2)
    print(f"\nTop matching projects:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.metadata['title']}")
    print()

if __name__ == "__main__":
    main()
