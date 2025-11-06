"""
RAGmail - Personalized Professor Outreach Email Generator
Main application interface
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from src.email_generator import EmailGenerator


def print_header():
    """Print application header."""
    print("=" * 80)
    print("RAGmail - AI-Powered Professor Outreach Email Generator")
    print("=" * 80)
    print()


def get_input(prompt: str, required: bool = True) -> str:
    """Get user input with optional requirement."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please enter a value.")


def save_email(email_data: dict, professor_name: str):
    """Save generated email to file."""
    output_dir = Path("generated_emails")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{professor_name.replace(' ', '_').replace('.', '')}_{timestamp}.txt"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Subject: {email_data['subject']}\n")
        f.write("=" * 80 + "\n\n")
        f.write(email_data['body'])
        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"\nMetadata:\n")
        f.write(f"  Template Type: {email_data['metadata']['template_type']}\n")
        f.write(f"  Selected Project: {email_data['metadata']['selected_project']}\n")
        f.write(f"  Relevance Score: {email_data['metadata']['relevance_score']}\n")
    
    print(f"\n✓ Email saved to: {filepath}")


def main():
    """Main application."""
    print_header()
    
    # Initialize generator
    print("Initializing RAGmail system...")
    try:
        generator = EmailGenerator()
        print("✓ System ready!\n")
    except FileNotFoundError:
        print("\n❌ Error: Vector database not initialized.")
        print("Please run: python src/vector_store.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error initializing system: {e}")
        sys.exit(1)
    
    while True:
        print("\n" + "-" * 80)
        print("Enter Professor Details")
        print("-" * 80 + "\n")
        
        # Collect professor information
        prof_name = get_input("Professor Name (e.g., Dr. John Smith): ")
        university = get_input("University Name: ")
        research_area = get_input("Research Domain/Areas: ")
        
        print("\nOptional Information (press Enter to skip):")
        paper_title = get_input("  Recent Paper Title: ", required=False)
        
        paper_summary = None
        if paper_title:
            paper_summary = get_input("  Paper Summary/Purpose: ", required=False)
        
        force_project = get_input("  Force Specific Project (name or ID): ", required=False)
        
        # Generate email
        print("\n🔄 Generating personalized email...")
        try:
            email = generator.generate_email(
                professor_name=prof_name,
                university_name=university,
                research_domain=research_area,
                paper_title=paper_title if paper_title else None,
                paper_summary=paper_summary if paper_summary else None,
                use_specific_project=force_project if force_project else None
            )
            
            # Display email
            print("\n" + "=" * 80)
            print("GENERATED EMAIL")
            print("=" * 80 + "\n")
            print(f"Subject: {email['subject']}\n")
            print(email['body'])
            print("\n" + "=" * 80)
            print(f"\n📊 Selected Project: {email['metadata']['selected_project']}")
            print(f"📈 Relevance Score: {email['metadata']['relevance_score']}")
            
            # Save option
            save_choice = get_input("\nSave this email? (y/n): ").lower()
            if save_choice == 'y':
                save_email(email, prof_name)
            
        except Exception as e:
            print(f"\n❌ Error generating email: {e}")
            import traceback
            traceback.print_exc()
        
        # Continue or exit
        print("\n" + "-" * 80)
        continue_choice = get_input("Generate another email? (y/n): ").lower()
        if continue_choice != 'y':
            print("\nThank you for using RAGmail! Good luck with your applications! 🎓")
            break


if __name__ == "__main__":
    main()
