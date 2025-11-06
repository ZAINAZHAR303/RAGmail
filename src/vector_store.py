"""
Vector store setup using ChromaDB for RAGmail system.
"""

from typing import List, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.document_loader import RAGmailDocumentLoader


class RAGmailVectorStore:
    """Manage vector store for semantic search."""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vectorstore: Optional[Chroma] = None
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """Create and persist vector store from documents."""
        print(f"Creating vector store with {len(documents)} documents...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Vector store created and persisted to {self.persist_directory}")
        return self.vectorstore
    
    def load_vectorstore(self) -> Chroma:
        """Load existing vector store."""
        if not Path(self.persist_directory).exists():
            raise FileNotFoundError(
                f"Vector store not found at {self.persist_directory}. "
                "Please create it first using create_vectorstore()."
            )
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        print(f"Loaded vector store from {self.persist_directory}")
        return self.vectorstore
    
    def search_similar(self, query: str, k: int = 3, filter_dict: Optional[dict] = None) -> List[Document]:
        """Search for similar documents."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Load or create it first.")
        
        if filter_dict:
            return self.vectorstore.similarity_search(query, k=k, filter=filter_dict)
        return self.vectorstore.similarity_search(query, k=k)
    
    def search_projects_only(self, query: str, k: int = 3) -> List[Document]:
        """Search only in projects."""
        return self.search_similar(query, k=k, filter_dict={"source": "projects"})


def initialize_vector_db():
    """Initialize vector database with all documents."""
    loader = RAGmailDocumentLoader()
    documents = loader.load_all_documents()
    
    vector_store = RAGmailVectorStore()
    vector_store.create_vectorstore(documents)
    
    return vector_store


if __name__ == "__main__":
    # Initialize the vector database
    print("Initializing RAGmail Vector Database...")
    vs = initialize_vector_db()
    
    # Test search
    print("\n=== Testing Search ===")
    test_query = "multi-agent systems and LangGraph"
    results = vs.search_projects_only(test_query, k=2)
    
    print(f"\nTop results for: '{test_query}'")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.metadata['title']}")
        print(f"   Type: {doc.metadata['type']}")
        print(f"   Domains: {', '.join(doc.metadata['domains'])}")
