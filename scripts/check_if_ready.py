"""
Quick script to check if the knowledge base is ready for queries.
Run this to see if indexing is complete before testing the chatbot.
"""
import os
import boto3
import json

REGION = os.getenv("AWS_REGION", "us-east-2")
KNOWLEDGE_BASE_ID = "YN0B2UVKBS"

runtime_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

def check_ready():
    """Check if knowledge base retrieval is working"""
    print("Checking if knowledge base is ready...")
    print("="*60)
    
    test_queries = ["NovaTech", "What is NovaTech", "industries"]
    
    for query in test_queries:
        try:
            resp = runtime_client.retrieve(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                retrievalQuery={"text": query},
                retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 1}}
            )
            
            results = resp.get("retrievalResults", [])
            
            if results:
                print(f"✅ SUCCESS! Knowledge base is ready!")
                print(f"   Query: '{query}'")
                print(f"   Results: {len(results)} found")
                
                # Show a snippet of the first result
                first_result = results[0]
                content = first_result.get("content", {})
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]
                    print(f"   Sample: {text[:100]}...")
                else:
                    print(f"   Sample: {str(content)[:100]}...")
                
                print("\n🎉 You can now test your chatbot!")
                return True
            else:
                print(f"⏳ Query '{query}': No results yet (still indexing...)")
        except Exception as e:
            print(f"❌ Error with query '{query}': {e}")
    
    print("\n" + "="*60)
    print("⏳ Knowledge base is still indexing. Please wait a bit longer.")
    print("   Try again in a few minutes.")
    return False

if __name__ == "__main__":
    check_ready()

