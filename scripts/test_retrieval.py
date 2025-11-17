"""
Test script to debug knowledge base retrieval
"""
import os
import json
import boto3

REGION = os.getenv("AWS_REGION", "us-east-2")
KNOWLEDGE_BASE_ID = "YN0B2UVKBS"

kb_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

def test_retrieval(query: str):
    """Test the retrieval and print the full response structure"""
    print(f"\n{'='*60}")
    print(f"Testing query: {query}")
    print(f"{'='*60}\n")
    
    try:
        resp = kb_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 5}}
        )
        
        print("Full Response Structure:")
        print(json.dumps(resp, indent=2, default=str))
        print("\n" + "-"*60 + "\n")
        
        results = resp.get("retrievalResults", [])
        print(f"Number of results: {len(results)}\n")
        
        for i, r in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Keys: {list(r.keys())}")
            print(f"  Full content: {json.dumps(r, indent=4, default=str)}")
            print()
            
            # Try different ways to extract text
            if "content" in r:
                content = r["content"]
                print(f"  Content type: {type(content)}")
                print(f"  Content keys: {list(content.keys()) if isinstance(content, dict) else 'N/A'}")
                if isinstance(content, dict):
                    if "text" in content:
                        print(f"  Text found: {content['text'][:200]}...")
                    else:
                        print(f"  No 'text' key in content")
            print()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_retrieval("What is NovaTech?")
    test_retrieval("What industries does NovaTech serve?")

