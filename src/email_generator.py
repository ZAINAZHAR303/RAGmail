"""
Email generation system for RAGmail.
Selects appropriate template and generates personalized emails.
"""

import os
from typing import Optional, Dict
from dotenv import load_dotenv
from src.document_loader import RAGmailDocumentLoader
from src.rag_chain import ProfessorProjectMatcher

load_dotenv()


class EmailGenerator:
    """Generate personalized emails for professors."""
    
    # Fixed sections that appear in every email
    SUBJECT = "Prospective Graduate Student | IELTS 7.0 | BSCS: CGPA (3.37/4.00) | SL@ Stanford CIP | 10X International Hackathons"
    
    HIGHLIGHTS = """A few highlights from my profile:
- Selected as Section Leader at Stanford University's Code in Place over 17,000+ global applicants to teach Python Programming.
- Winner, Harvard CS50 Puzzle Day 2025
- Participant in 10+ international AI hackathons (Lablab.ai)
- Ranked 99th globally at M{IT}2 Informatics Tournament 2025
- Ranked participant in Meta Hacker Cup 2024 (13k+ competitors)
- Voluntarily taught 30+ hours of Web Development and IELTS to underprivileged students."""
    
    CLOSING = """I have attached my CV and relevant documents for your review. I would be truly grateful for an opportunity to discuss how my background and research interests could align with your group's ongoing projects.

Best regards,
Zain Azhar"""
    
    def __init__(self):
        self.matcher = ProfessorProjectMatcher()
        self.loader = RAGmailDocumentLoader()
    
    def _select_template_type(
        self, 
        has_paper: bool,
        use_specific_project: Optional[str] = None
    ) -> int:
        """
        Select which template to use.
        1: Generic (no paper reference)
        2: Paper-referenced with generic project
        3: Paper-referenced with specific project (like HireFlow)
        """
        if not has_paper:
            return 1
        elif use_specific_project:
            return 3
        else:
            return 2
    
    def generate_email(
        self,
        professor_name: str,
        university_name: str,
        research_domain: str,
        paper_title: Optional[str] = None,
        paper_summary: Optional[str] = None,
        use_specific_project: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a personalized email.
        
        Args:
            professor_name: Full name (e.g., "John Smith" or "Dr. John Smith")
            university_name: Name of the university
            research_domain: Professor's research area
            paper_title: Optional recent paper title
            paper_summary: Optional paper summary/purpose
            use_specific_project: Optional project ID to force use of specific project
        
        Returns:
            Dict with 'subject', 'body', and 'metadata'
        """
        
        # Determine template
        has_paper = paper_title is not None
        template_type = self._select_template_type(has_paper, use_specific_project)
        
        # Get matching project and generate paragraph
        if use_specific_project:
            # Force specific project
            matching_projects = self.matcher.find_matching_projects(research_domain, paper_title, k=5)
            # Find the requested project
            selected = None
            for proj in matching_projects:
                if proj.metadata['project_id'] == use_specific_project or \
                   proj.metadata['title'].lower() == use_specific_project.lower():
                    selected = {
                        "project_document": proj,
                        "project_title": proj.metadata['title'],
                        "alignment_explanation": "Specifically requested project"
                    }
                    break
            
            if selected is None:
                # Fallback to best match
                selected = self.matcher.select_best_project(
                    research_domain, paper_title, paper_summary, matching_projects
                )
        else:
            # Auto-select best project
            matching_projects = self.matcher.find_matching_projects(research_domain, paper_title, k=3)
            selected = self.matcher.select_best_project(
                research_domain, paper_title, paper_summary, matching_projects
            )
        
        # Generate project paragraph
        project_paragraph = self.matcher.generate_project_paragraph(
            professor_name.replace("Dr. ", "").replace("Professor ", ""),
            research_domain,
            paper_title,
            paper_summary,
            selected
        )
        
        # Build email based on template type
        if template_type == 1:
            # Generic template
            body = self._generate_generic_email(
                professor_name, university_name, research_domain, project_paragraph
            )
        elif template_type == 2:
            # Paper-referenced generic
            body = self._generate_paper_generic_email(
                professor_name, university_name, research_domain, 
                paper_title, paper_summary, project_paragraph
            )
        else:
            # Paper-referenced with specific project
            body = self._generate_paper_specific_email(
                professor_name, university_name, research_domain,
                paper_title, paper_summary, project_paragraph
            )
        
        return {
            "subject": self.SUBJECT,
            "body": body,
            "metadata": {
                "template_type": template_type,
                "selected_project": selected["project_title"],
                "relevance_score": selected.get("relevance_score", "N/A")
            }
        }
    
    def _generate_generic_email(
        self, prof_name: str, university: str, research_area: str, project_para: str
    ) -> str:
        """Template 1: Generic email without paper reference."""
        return f"""Dear {prof_name},

I hope this message finds you well. My name is Zain Azhar, and I am a final-year Computer Science undergraduate at the University of Agriculture Faisalabad. I am very interested in pursuing graduate research under your supervision at {university}, particularly in the areas of {research_area}.

{project_para}

{self.HIGHLIGHTS}

{self.CLOSING}"""
    
    def _generate_paper_generic_email(
        self, prof_name: str, university: str, research_area: str,
        paper_title: str, paper_summary: Optional[str], project_para: str
    ) -> str:
        """Template 2: Paper-referenced with generic project alignment."""
        paper_line = f'I was particularly interested in your recent paper, "{paper_title}"'
        if paper_summary:
            paper_line += f", which addresses {paper_summary}."
        else:
            paper_line += "."
        
        return f"""Dear {prof_name},

I hope this message finds you well. My name is Zain Azhar, and I am a final-year Computer Science undergraduate at the University of Agriculture Faisalabad. I am eager to contribute to research under your supervision in the field of {research_area} as a prospective graduate student at {university}.

{paper_line} {project_para}

{self.HIGHLIGHTS}

I have attached my CV and relevant documents for your review. I would be happy to arrange a virtual meeting at your convenience.

Best regards,
Zain Azhar"""
    
    def _generate_paper_specific_email(
        self, prof_name: str, university: str, research_area: str,
        paper_title: str, paper_summary: Optional[str], project_para: str
    ) -> str:
        """Template 3: Paper-referenced with specific project."""
        return self._generate_paper_generic_email(
            prof_name, university, research_area, paper_title, paper_summary, project_para
        )


if __name__ == "__main__":
    # Test email generation
    generator = EmailGenerator()
    
    print("=== Test Case 1: Generic Email ===\n")
    email1 = generator.generate_email(
        professor_name="Dr. Sarah Johnson",
        university_name="Stanford University",
        research_domain="artificial intelligence, machine learning, and computer vision"
    )
    print(f"Subject: {email1['subject']}\n")
    print(email1['body'])
    print(f"\nMetadata: {email1['metadata']}")
    
    print("\n\n" + "="*80 + "\n")
    print("=== Test Case 2: With Paper Reference ===\n")
    email2 = generator.generate_email(
        professor_name="Dr. Michael Chen",
        university_name="MIT",
        research_domain="multi-agent systems and natural language processing",
        paper_title="Coordinated Multi-Agent Planning for Complex Tasks",
        paper_summary="explores coordination mechanisms for distributed AI agents"
    )
    print(f"Subject: {email2['subject']}\n")
    print(email2['body'])
    print(f"\nMetadata: {email2['metadata']}")
