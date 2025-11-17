# Project Structure

```
rag-agentcore/
│
├── app.py                          # Main application (RAG chatbot server)
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── LICENSE                          # MIT License
├── .gitignore                      # Git ignore rules
├── .gitattributes                   # Git attributes for line endings
│
├── config.example.py               # Example configuration (copy to config.py)
├── SETUP_GITHUB.md                 # GitHub setup instructions
├── KNOWLEDGE_BASE_SETUP.md         # Knowledge base setup guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── PROJECT_STRUCTURE.md            # This file
│
├── scripts/                         # Helper scripts
│   ├── sync_knowledge_base.py      # Sync KB data source
│   ├── check_if_ready.py          # Check if KB is ready
│   ├── check_kb_status.py         # Check KB status
│   ├── serve_test_page.py          # Serve test page
│   └── test_retrieval.py           # Test retrieval function
│
├── knowledge/                       # Sample knowledge base files
│   ├── company_overview.txt
│   ├── faq.txt
│   └── product_specs.txt
│
└── test_page.html                  # Interactive test page for the chatbot
```

## File Descriptions

### Core Application
- **app.py**: Main RAG chatbot application using Bedrock Agent Core
- **requirements.txt**: Python package dependencies

### Documentation
- **README.md**: Complete project documentation with setup and usage instructions
- **KNOWLEDGE_BASE_SETUP.md**: Detailed guide for setting up AWS Bedrock Knowledge Base
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **SETUP_GITHUB.md**: Instructions for pushing to GitHub

### Configuration
- **config.example.py**: Example configuration file (copy to config.py and update)
- **.gitignore**: Excludes virtual environments, cache files, credentials, etc.
- **.gitattributes**: Ensures consistent line endings across platforms

### Scripts
- **sync_knowledge_base.py**: Syncs and checks knowledge base data sources
- **check_if_ready.py**: Quick check if knowledge base is ready for queries
- **check_kb_status.py**: Detailed knowledge base status check
- **serve_test_page.py**: HTTP server for the test page (avoids CORS issues)
- **test_retrieval.py**: Debug script to test retrieval function

### Knowledge Base Files
Sample files that can be uploaded to your knowledge base:
- **company_overview.txt**: Company information
- **faq.txt**: Frequently asked questions
- **product_specs.txt**: Product specifications

### Frontend
- **test_page.html**: Beautiful, interactive test page for the chatbot

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables or update `app.py` with your Knowledge Base ID
3. Sync knowledge base: `python scripts/sync_knowledge_base.py`
4. Start server: `python app.py`
5. Test: `python scripts/serve_test_page.py`

## Notes

- The `.venv/` directory is ignored by git (virtual environment)
- Configuration files with sensitive data are in `.gitignore`
- All scripts are in the `scripts/` directory for organization
- Knowledge base files are samples - replace with your own data
