import os
import json
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import boto3
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

# ---------- Config ----------
REGION = os.getenv("AWS_REGION", "us-east-2")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "YN0B2UVKBS")  # Set via environment variable

# ---------- Clients ----------
kb_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

# ---------- Retrieval ----------
def retrieve_from_kb(query: str, top_k: int = 5) -> str:
    """
    Calls Bedrock Knowledge Base 'Retrieve' to get the most relevant text chunks.
    Returns a single string with all retrieved texts joined together.
    """
    try:
        resp = kb_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": top_k}}
        )
        results = resp.get("retrievalResults", [])
        
        if not results:
            # Log warning but don't fail - return empty string
            print(f"Warning: No results retrieved from knowledge base for query: {query}")
            return ""
        
        texts = []
        for r in results:
            # Try different possible structures for the content
            content = r.get("content", {})
            
            # Handle different content formats
            if isinstance(content, dict):
                # Standard format: content.text
                if "text" in content:
                    texts.append(content["text"])
                # Alternative: content might be the text directly
                elif len(content) == 1 and list(content.values())[0]:
                    texts.append(str(list(content.values())[0]))
            elif isinstance(content, str):
                # Content is already a string
                texts.append(content)
            else:
                # Fallback: try to get text from other possible locations
                if "text" in r:
                    texts.append(r["text"])
                elif "body" in r:
                    texts.append(str(r["body"]))
        
        if texts:
            return "\n\n---\n\n".join(texts)
        else:
            print(f"Warning: Could not extract text from retrieval results. Raw result: {r}")
            return ""
            
    except Exception as e:
        print(f"Error retrieving from knowledge base: {e}")
        import traceback
        traceback.print_exc()
        return ""

# ---------- Agent ----------
app = BedrockAgentCoreApp()
agent = Agent()   # default chat-style agent

# ---------- CORS Middleware ----------
# Allow CORS for browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.entrypoint
def invoke(payload):
    user_prompt = payload.get("prompt", "").strip()
    
    # Retrieve context from knowledge base
    context = retrieve_from_kb(user_prompt) if user_prompt else ""
    
    # Build the prompt with context
    if context:
        combined = (
            "You are a helpful assistant for NovaTech Solutions. Use ONLY the information provided in the CONTEXT below to answer the question.\n\n"
            f"CONTEXT FROM KNOWLEDGE BASE:\n{context}\n\n"
            f"QUESTION: {user_prompt}\n\n"
            "INSTRUCTIONS:\n"
            "- Answer based ONLY on the context provided above\n"
            "- If the context contains the answer, provide a clear and concise response\n"
            "- If the context doesn't contain enough information, say 'I don't have enough information in the knowledge base to answer this question.'\n"
            "- Do not make up information or use knowledge outside of the provided context"
        )
    else:
        combined = (
            "You are a helpful assistant for NovaTech Solutions.\n\n"
            f"QUESTION: {user_prompt}\n\n"
            "I don't have enough information in the knowledge base to answer this question. "
            "Please make sure the knowledge base has been synced and contains relevant information."
        )

    result = agent(combined)
    # Normalize to plain text
    try:
        text = result.message["content"][0]["text"]
    except Exception:
        text = str(result.message)
    return {"result": text}

# ---------- Additional Routes ----------
@app.route("/", methods=["GET"])
async def root(request):
    return JSONResponse({
        "message": "Bedrock Agent RAG API is running",
        "endpoints": {
            "/": "This information page (GET)",
            "/health": "Health check (GET)",
            "/invocations": "Main entrypoint - send POST request with JSON body: {\"prompt\": \"your question here\"}"
        },
        "example_curl": "curl -X POST http://127.0.0.1:18080/invocations -H 'Content-Type: application/json' -d '{\"prompt\": \"What is NovaTech?\"}'"
    })

@app.route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy"})

@app.route("/debug/retrieval", methods=["POST"])
async def debug_retrieval(request):
    """Debug endpoint to test knowledge base retrieval"""
    try:
        data = await request.json()
        query = data.get("query", "NovaTech")
        
        # Test retrieval
        context = retrieve_from_kb(query, top_k=3)
        
        # Also get raw response for debugging
        try:
            resp = kb_client.retrieve(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                retrievalQuery={"text": query},
                retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 3}}
            )
            raw_results = resp.get("retrievalResults", [])
        except Exception as e:
            raw_results = []
            error = str(e)
        
        return JSONResponse({
            "query": query,
            "context_retrieved": context[:500] if context else "No context retrieved",
            "context_length": len(context) if context else 0,
            "num_results": len(raw_results),
            "raw_results_count": len(raw_results),
            "knowledge_base_id": KNOWLEDGE_BASE_ID,
            "status": "success" if context else "no_results"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # Use a high port to avoid conflicts on Windows dev machines
    app.run(host="127.0.0.1", port=18080)
