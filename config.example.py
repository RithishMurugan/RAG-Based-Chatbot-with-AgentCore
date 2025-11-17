"""
Example configuration file.
Copy this to config.py and update with your values.
DO NOT commit config.py to git (it's in .gitignore)
"""

# AWS Configuration
AWS_REGION = "us-east-2"  # Your AWS region

# Knowledge Base Configuration
KNOWLEDGE_BASE_ID = "YOUR_KNOWLEDGE_BASE_ID_HERE"  # Your Bedrock Knowledge Base ID

# Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 18080

# Retrieval Configuration
TOP_K_RESULTS = 5  # Number of results to retrieve from knowledge base
