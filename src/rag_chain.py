"""
RAG Chain for professor-project matching using LangChain and Groq.
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from src.vector_store import RAGmailVectorStore

load_dotenv()


class ProfessorProjectMatcher:
    """Match professor research with relevant projects using RAG."""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.vector_store = RAGmailVectorStore()
        
        # Try to load existing vector store
        try:
            self.vector_store.load_vectorstore()
        except FileNotFoundError:
            print("Vector store not found. Please run initialize_vector_db first.")
            raise
    
    def find_matching_projects(
        self, 
        professor_research: str, 
        paper_title: Optional[str] = None,
        k: int = 3
    ) -> List[Document]:
        """Find projects that match professor's research area."""
        
        # Build search query
        query = professor_research
        if paper_title:
            query = f"{professor_research}. Recent paper: {paper_title}"
        
        # Search for matching projects
        matching_projects = self.vector_store.search_projects_only(query, k=k)
        
        return matching_projects
    
    def select_best_project(
        self,
        professor_research: str,
        paper_title: Optional[str] = None,
        paper_summary: Optional[str] = None,
        matching_projects: Optional[List[Document]] = None
    ) -> Dict:
        """Use LLM to select and explain the best matching project."""
        
        if matching_projects is None:
            matching_projects = self.find_matching_projects(professor_research, paper_title)
        
        # Prepare context
        projects_context = "\n\n".join([
            f"PROJECT {i+1}:\n{doc.page_content}\n"
            for i, doc in enumerate(matching_projects)
        ])
        
        # Create prompt
        selection_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at matching student projects with professor research interests.
Your task is to analyze the professor's research area and select the MOST RELEVANT project from the student's portfolio.

Consider:
- Technical alignment (technologies, methods, domains)
- Research area overlap
- Demonstrated skills relevant to the professor's work
- Impact and sophistication of the project

Respond in JSON format with:
{{
    "selected_project_number": <1, 2, or 3>,
    "project_title": "<title>",
    "alignment_explanation": "<2-3 sentences explaining why this project aligns with the professor's research>",
    "key_technologies": ["tech1", "tech2", ...],
    "relevance_score": <1-10>
}}
"""),
            ("user", """Professor's Research Area: {research_area}
{paper_info}

Available Projects:
{projects}

Select the best matching project and explain the alignment.""")
        ])
        
        paper_info = ""
        if paper_title:
            paper_info = f"Recent Paper: {paper_title}"
            if paper_summary:
                paper_info += f"\nPaper Summary: {paper_summary}"
        
        chain = selection_prompt | self.llm
        
        response = chain.invoke({
            "research_area": professor_research,
            "paper_info": paper_info,
            "projects": projects_context
        })
        
        # Parse response (handle both JSON and text)
        try:
            import json
            result = json.loads(response.content)
        except:
            # Fallback: extract information from text response
            selected_idx = 0
            result = {
                "selected_project_number": 1,
                "project_title": matching_projects[selected_idx].metadata['title'],
                "alignment_explanation": response.content,
                "key_technologies": matching_projects[selected_idx].metadata.get('domains', []),
                "relevance_score": 8
            }
        
        # Add full project document
        selected_idx = result.get("selected_project_number", 1) - 1
        result["project_document"] = matching_projects[selected_idx]
        
        return result
    
    def generate_project_paragraph(
        self,
        professor_name: str,
        professor_research: str,
        paper_title: Optional[str] = None,
        paper_summary: Optional[str] = None,
        selected_project: Optional[Dict] = None
    ) -> str:
        """Generate the project alignment paragraph for email."""
        
        if selected_project is None:
            matching_projects = self.find_matching_projects(professor_research, paper_title)
            selected_project = self.select_best_project(
                professor_research, paper_title, paper_summary, matching_projects
            )
        
        project_doc = selected_project["project_document"]
        project_title = selected_project["project_title"]
        
        # Create paragraph generation prompt
        paragraph_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are writing a compelling paragraph for a graduate school application email.
The paragraph should:
1. Reference the professor's research or paper naturally
2. Describe the student's relevant project in 2-3 sentences
3. Highlight the technical alignment and demonstrated skills
4. Be professional, specific, and show genuine interest
5. Use active voice and concrete details

Keep it concise (3-4 sentences max) and authentic."""),
            ("user", """Professor: Dr. {professor_name}
Professor's Research: {research_area}
{paper_info}

Student's Selected Project:
Title: {project_title}
{project_details}

Alignment Reasoning: {alignment_explanation}

Write a compelling paragraph connecting this project to the professor's work.""")
        ])
        
        paper_info = ""
        if paper_title:
            paper_info = f'Recent Paper: "{paper_title}"'
            if paper_summary:
                paper_info += f"\n{paper_summary}"
        
        chain = paragraph_prompt | self.llm
        
        response = chain.invoke({
            "professor_name": professor_name,
            "research_area": professor_research,
            "paper_info": paper_info,
            "project_title": project_title,
            "project_details": project_doc.page_content[:800],  # Truncate for context
            "alignment_explanation": selected_project["alignment_explanation"]
        })
        
        return response.content.strip()


if __name__ == "__main__":
    # Test the matcher
    matcher = ProfessorProjectMatcher()
    
    # Test case
    test_research = "multi-agent systems, natural language processing, and intelligent agents"
    test_paper = "Coordinated Multi-Agent Systems for Task Automation"
    
    print("=== Testing Project Matcher ===\n")
    print(f"Research Area: {test_research}")
    print(f"Paper: {test_paper}\n")
    
    # Find matches
    projects = matcher.find_matching_projects(test_research, test_paper, k=3)
    print(f"Found {len(projects)} matching projects:")
    for i, proj in enumerate(projects, 1):
        print(f"{i}. {proj.metadata['title']}")
    
    # Select best
    print("\n=== Selecting Best Project ===")
    best = matcher.select_best_project(test_research, test_paper, matching_projects=projects)
    print(f"Selected: {best['project_title']}")
    print(f"Relevance: {best['relevance_score']}/10")
    print(f"Reasoning: {best['alignment_explanation']}")
    
    # Generate paragraph
    print("\n=== Generated Paragraph ===")
    paragraph = matcher.generate_project_paragraph(
        "Smith", test_research, test_paper, selected_project=best
    )
    print(paragraph)
