# RAG Agent Core - Bedrock Knowledge Base Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with AWS Bedrock Agent Core and Knowledge Base. This application uses AWS Bedrock's Knowledge Base to retrieve relevant context and generates responses using Strands Agents.

## Features

- 🤖 **RAG-powered chatbot** using AWS Bedrock Knowledge Base
- 🔍 **Semantic search** to retrieve relevant context from your documents
- 🌐 **RESTful API** with CORS support for web applications
- 🎨 **Interactive test page** for easy testing
- 🐛 **Debug endpoints** for troubleshooting
- ⚡ **Fast and efficient** retrieval with configurable top-k results

## Architecture

```
User Query → Bedrock Knowledge Base (Retrieve) → Context + Query → Strands Agent → Response
```

1. User sends a query
2. System retrieves relevant context from AWS Bedrock Knowledge Base
3. Context and query are combined into a prompt
4. Strands Agent generates a response based on the context
5. Response is returned to the user

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS Bedrock Knowledge Base created and configured
- AWS credentials configured (via `~/.aws/credentials` or environment variables)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-agentcore
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Set your AWS region
   export AWS_REGION=us-east-2
   
   # Set your Knowledge Base ID (optional, can be set in app.py)
   export KNOWLEDGE_BASE_ID=your-kb-id-here
   ```

5. **Update Knowledge Base ID**
   
   Edit `app.py` and update the `KNOWLEDGE_BASE_ID` variable with your knowledge base ID:
   ```python
   KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "YOUR_KB_ID_HERE")
   ```

## Usage

### 1. Sync Your Knowledge Base

Before using the chatbot, ensure your knowledge base is synced and indexed:

```bash
python scripts/sync_knowledge_base.py
```

Wait 5-15 minutes for indexing to complete. Check status with:

```bash
python scripts/check_if_ready.py
```

### 2. Start the Server

```bash
python app.py
```

The server will start on `http://127.0.0.1:18080`

### 3. Test the API

**Using curl:**
```bash
curl -X POST http://127.0.0.1:18080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is NovaTech?"}'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:18080/invocations",
    json={"prompt": "What is NovaTech?"}
)
print(response.json()["result"])
```

### 4. Use the Test Page

1. Start the test page server:
   ```bash
   python scripts/serve_test_page.py
   ```

2. Open your browser to `http://127.0.0.1:8080/test_page.html`

3. Enter questions and get responses!

## API Endpoints

### `POST /invocations`
Main endpoint for chatbot queries.

**Request:**
```json
{
  "prompt": "Your question here"
}
```

**Response:**
```json
{
  "result": "Answer from the chatbot"
}
```

### `GET /`
API information page showing available endpoints.

### `GET /health`
Health check endpoint.

### `POST /debug/retrieval`
Debug endpoint to test knowledge base retrieval.

**Request:**
```json
{
  "query": "test query"
}
```

## Project Structure

```
rag-agentcore/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                 # Git ignore rules
├── scripts/                    # Helper scripts
│   ├── sync_knowledge_base.py  # Sync knowledge base
│   ├── check_if_ready.py      # Check if KB is ready
│   ├── serve_test_page.py      # Serve test page
│   └── check_kb_status.py     # Check KB status
├── Knowledge/                  # Sample knowledge base files
│   ├── company_overview.txt
│   ├── faq.txt
│   └── product_specs.txt
└── test_page.html              # Interactive test page
```

## Configuration

### Environment Variables

- `AWS_REGION`: AWS region (default: `us-east-2`)
- `KNOWLEDGE_BASE_ID`: Your Bedrock Knowledge Base ID (can also be set in `app.py`)

### Knowledge Base Setup

1. Create a Knowledge Base in AWS Bedrock Console
2. Add a data source (S3 bucket, etc.)
3. Upload your documents to the data source
4. Sync the data source (can take 5-15 minutes)
5. Update `KNOWLEDGE_BASE_ID` in `app.py` or set as environment variable

See `KNOWLEDGE_BASE_SETUP.md` for detailed setup instructions.

## Troubleshooting

### No results from knowledge base

1. **Check if knowledge base is synced:**
   ```bash
   python scripts/check_if_ready.py
   ```

2. **Verify sync status in AWS Console:**
   - Go to Amazon Bedrock → Knowledge bases
   - Check data source sync status

3. **Test retrieval directly:**
   ```bash
   curl -X POST http://127.0.0.1:18080/debug/retrieval \
     -H "Content-Type: application/json" \
     -d '{"query": "test"}'
   ```

### CORS errors

The server includes CORS middleware. If you still see errors:
- Make sure you're serving the HTML file via HTTP (use `scripts/serve_test_page.py`)
- Don't open HTML files directly (file:// protocol)

### AWS credentials

Ensure your AWS credentials are configured:
```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=us-east-2
```

## Development

### Adding New Features

- Main application logic: `app.py`
- Retrieval function: `retrieve_from_kb()` in `app.py`
- Agent configuration: Modify the prompt in `invoke()` function

### Testing

Test the knowledge base retrieval:
```bash
python scripts/test_retrieval.py
```

Check knowledge base status:
```bash
python scripts/check_kb_status.py
```


## Acknowledgments

- Built with [AWS Bedrock Agent Core](https://aws.amazon.com/bedrock/)
- Uses [Strands Agents](https://github.com/strands-ai/strands) for LLM interactions
- Knowledge Base retrieval powered by AWS Bedrock

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review AWS Bedrock documentation
3. Open an issue on GitHub
