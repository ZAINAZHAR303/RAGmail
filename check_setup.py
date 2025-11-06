"""
Quick setup verification script
"""

print("Checking installations...")

try:
    import langchain_core
    print("✓ langchain-core installed")
except:
    print("✗ langchain-core NOT installed")

try:
    import langchain_groq
    print("✓ langchain-groq installed")
except:
    print("✗ langchain-groq NOT installed")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv installed")
except:
    print("✗ python-dotenv NOT installed")

try:
    import chromadb
    print("✓ chromadb installed")
except:
    print("✗ chromadb NOT installed")

try:
    from sentence_transformers import SentenceTransformer
    print("✓ sentence-transformers installed")
except:
    print("✗ sentence-transformers NOT installed")

print("\nData files check:")
import os
data_files = ["projects.json", "achievements.txt", "research_interests.txt", 
              "skills.txt", "coursework.txt", "email_templates.txt"]

for file in data_files:
    path = f"data/{file}"
    if os.path.exists(path):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} MISSING")

print("\nSetup verification complete!")
