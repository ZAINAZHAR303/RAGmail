"""
Document loader for RAGmail system.
Loads and chunks projects, achievements, skills, and other background data.
"""

import json
from pathlib import Path
from typing import List, Dict
from langchain.schema import Document


class RAGmailDocumentLoader:
    """Load and prepare documents for RAG system."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
    
    def load_projects(self) -> List[Document]:
        """Load projects from JSON and create documents."""
        projects_path = self.data_dir / "projects.json"
        
        with open(projects_path, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        documents = []
        for project in projects:
            # Create rich text representation for better semantic search
            content = f"""
Project: {project['title']}
Type: {project['type']}
Domain: {', '.join(project['domain'])}
Technologies: {', '.join(project['technologies'])}

Description: {project['description']}

Detailed Overview: {project['detailed_description']}

Impact: {project['impact']}

Key Features:
{chr(10).join('- ' + feature for feature in project['key_features'])}

Research Keywords: {', '.join(project['research_keywords'])}
"""
            
            metadata = {
                "source": "projects",
                "project_id": project['id'],
                "title": project['title'],
                "type": project['type'],
                "domains": project['domain'],
                "keywords": project['research_keywords']
            }
            
            if 'github' in project:
                metadata['github'] = project['github']
            if 'demo' in project:
                metadata['demo'] = project['demo']
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    
    def load_text_file(self, filename: str, source_type: str) -> List[Document]:
        """Load a text file and create a document."""
        file_path = self.data_dir / filename
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return [Document(
            page_content=content,
            metadata={"source": source_type, "filename": filename}
        )]
    
    def load_all_documents(self) -> List[Document]:
        """Load all documents for the RAG system."""
        documents = []
        
        # Load projects (most important for matching)
        documents.extend(self.load_projects())
        
        # Load other background data
        documents.extend(self.load_text_file("achievements.txt", "achievements"))
        documents.extend(self.load_text_file("research_interests.txt", "research_interests"))
        documents.extend(self.load_text_file("skills.txt", "skills"))
        documents.extend(self.load_text_file("coursework.txt", "coursework"))
        
        return documents
    
    def load_email_templates(self) -> str:
        """Load email templates separately (not for vector DB)."""
        templates_path = self.data_dir / "email_templates.txt"
        
        with open(templates_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == "__main__":
    # Test the loader
    loader = RAGmailDocumentLoader()
    docs = loader.load_all_documents()
    print(f"Loaded {len(docs)} documents")
    
    # Show first project
    print("\n=== Sample Project Document ===")
    print(docs[0].page_content[:500])
    print(f"\nMetadata: {docs[0].metadata}")
