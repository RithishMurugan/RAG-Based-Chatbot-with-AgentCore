"""
Check knowledge base status and configuration
"""
import os
import boto3
import json

REGION = os.getenv("AWS_REGION", "us-east-2")
KNOWLEDGE_BASE_ID = "YN0B2UVKBS"

# Use bedrock-agent client to check KB details
agent_client = boto3.client("bedrock-agent", region_name=REGION)
runtime_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

try:
    print(f"Checking Knowledge Base: {KNOWLEDGE_BASE_ID}")
    print("="*60)
    
    # Get knowledge base details
    kb_details = agent_client.get_knowledge_base(knowledgeBaseId=KNOWLEDGE_BASE_ID)
    
    print("\nKnowledge Base Details:")
    print(f"  Name: {kb_details.get('knowledgeBase', {}).get('name', 'N/A')}")
    print(f"  Status: {kb_details.get('knowledgeBase', {}).get('status', 'N/A')}")
    print(f"  Description: {kb_details.get('knowledgeBase', {}).get('description', 'N/A')}")
    
    # Check data sources
    print("\nData Sources:")
    data_sources = agent_client.list_data_sources(knowledgeBaseId=KNOWLEDGE_BASE_ID)
    for ds in data_sources.get('dataSourceSummaries', []):
        print(f"  - {ds.get('name', 'N/A')} (ID: {ds.get('dataSourceId', 'N/A')})")
        print(f"    Status: {ds.get('status', 'N/A')}")
        
        # Check sync jobs
        sync_jobs = agent_client.list_data_source_sync_jobs(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=ds.get('dataSourceId', '')
        )
        if sync_jobs.get('dataSourceSyncJobSummaries'):
            latest = sync_jobs['dataSourceSyncJobSummaries'][0]
            print(f"    Latest Sync: {latest.get('status', 'N/A')} - {latest.get('startedAt', 'N/A')}")
        print()
    
    print("\n" + "="*60)
    print("\nTrying retrieval with different query...")
    
    # Try a very simple query
    resp = runtime_client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": "NovaTech"},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 3}}
    )
    
    print(f"Retrieval results: {len(resp.get('retrievalResults', []))} results")
    if resp.get('retrievalResults'):
        print("✓ Retrieval is working!")
    else:
        print("✗ No results - Knowledge base may need to be synced/indexed")
        print("\nPossible issues:")
        print("  1. Data sources haven't been synced yet")
        print("  2. Knowledge base is still indexing")
        print("  3. Files haven't been uploaded to the data source")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

