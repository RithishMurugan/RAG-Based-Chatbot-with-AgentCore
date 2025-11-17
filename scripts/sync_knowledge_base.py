"""
Script to sync/start a sync job for the knowledge base data source.
This ensures the files are indexed and available for retrieval.
"""
import os
import boto3
import time

REGION = os.getenv("AWS_REGION", "us-east-2")
KNOWLEDGE_BASE_ID = "YN0B2UVKBS"

agent_client = boto3.client("bedrock-agent", region_name=REGION)
runtime_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

def list_data_sources():
    """List all data sources for the knowledge base"""
    try:
        response = agent_client.list_data_sources(knowledgeBaseId=KNOWLEDGE_BASE_ID)
        return response.get('dataSourceSummaries', [])
    except Exception as e:
        print(f"Error listing data sources: {e}")
        return []

def start_sync_job(knowledge_base_id, data_source_id):
    """Start a sync job for a data source"""
    try:
        response = agent_client.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id
        )
        return response.get('ingestionJob', {})
    except Exception as e:
        # Try alternative method name
        try:
            response = agent_client.start_data_source_sync_job(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id
            )
            return response
        except Exception as e2:
            print(f"Error starting sync job: {e}")
            print(f"Alternative method also failed: {e2}")
            return None

def check_sync_status(knowledge_base_id, data_source_id, job_id=None):
    """Check the status of sync jobs"""
    try:
        # Try to get ingestion job status
        if job_id:
            try:
                response = agent_client.get_ingestion_job(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    ingestionJobId=job_id
                )
                return response.get('ingestionJob', {})
            except:
                pass
        
        # List recent jobs
        try:
            response = agent_client.list_ingestion_jobs(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                maxResults=5
            )
            jobs = response.get('ingestionJobSummaries', [])
            if jobs:
                return jobs[0]  # Return most recent
        except:
            pass
        
        return None
    except Exception as e:
        print(f"Error checking sync status: {e}")
        return None

def test_retrieval():
    """Test if retrieval is working"""
    try:
        resp = runtime_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": "NovaTech"},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 1}}
        )
        return len(resp.get("retrievalResults", [])) > 0
    except Exception as e:
        print(f"Retrieval test error: {e}")
        return False

def main():
    print("="*60)
    print("Knowledge Base Sync Helper")
    print("="*60)
    print(f"Knowledge Base ID: {KNOWLEDGE_BASE_ID}")
    print(f"Region: {REGION}\n")
    
    # List data sources
    print("Checking data sources...")
    data_sources = list_data_sources()
    
    if not data_sources:
        print("❌ No data sources found!")
        print("\nPlease ensure:")
        print("  1. You have created a data source in your knowledge base")
        print("  2. Files have been uploaded to the data source location (S3, etc.)")
        return
    
    for ds in data_sources:
        print(f"\n📁 Data Source: {ds.get('name', 'N/A')}")
        print(f"   ID: {ds.get('dataSourceId', 'N/A')}")
        print(f"   Status: {ds.get('status', 'N/A')}")
        
        # Try to start a sync job
        print(f"\n   Attempting to start sync job...")
        job = start_sync_job(KNOWLEDGE_BASE_ID, ds.get('dataSourceId'))
        
        if job:
            print(f"   ✓ Sync job started!")
            print(f"   Job ID: {job.get('ingestionJobId', 'N/A')}")
            print(f"   Status: {job.get('status', 'N/A')}")
        else:
            print(f"   ⚠ Could not start sync job automatically.")
            print(f"   Please sync the data source manually in the AWS Console:")
            print(f"   - Go to Amazon Bedrock > Knowledge bases")
            print(f"   - Select your knowledge base")
            print(f"   - Go to Data sources tab")
            print(f"   - Click 'Sync' for the data source")
    
    print("\n" + "="*60)
    print("Testing retrieval...")
    
    if test_retrieval():
        print("✓ Retrieval is working! Your knowledge base is ready.")
    else:
        print("✗ Retrieval returned no results.")
        print("\nPossible solutions:")
        print("  1. Wait a few minutes for indexing to complete")
        print("  2. Manually sync the data source in AWS Console")
        print("  3. Verify files are in the data source location (S3 bucket, etc.)")
        print("  4. Check that the data source has the correct permissions")

if __name__ == "__main__":
    main()

