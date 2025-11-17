# GitHub Setup Checklist

Before pushing to GitHub, make sure to:

## ✅ Pre-Push Checklist

1. **Update Knowledge Base ID** (if you want to keep it private)
   - Edit `app.py` line 11
   - Replace `"YN0B2UVKBS"` with a placeholder or environment variable
   - Or use environment variable: `export KNOWLEDGE_BASE_ID=your-id`

2. **Review .gitignore**
   - Ensure sensitive files are excluded
   - Check that `.venv/`, `__pycache__/`, `.env` are ignored

3. **Test the application**
   ```bash
   python app.py
   ```

4. **Verify file structure**
   ```
   rag-agentcore/
   ├── app.py
   ├── requirements.txt
   ├── README.md
   ├── .gitignore
   ├── scripts/
   ├── knowledge/
   └── test_page.html
   ```

## 🚀 Push to GitHub

1. **Initialize git repository** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit: RAG Agent Core with Bedrock Knowledge Base"
   ```

2. **Add remote and push**
   ```bash
   git remote add origin https://github.com/your-username/rag-agentcore.git
   git branch -M main
   git push -u origin main
   ```

## 📝 Recommended Repository Settings

- Add description: "RAG-powered chatbot using AWS Bedrock Knowledge Base"
- Add topics: `aws`, `bedrock`, `rag`, `chatbot`, `python`, `knowledge-base`
- Enable Issues and Discussions
- Add a repository description

## 🔒 Security Notes

- **Never commit:**
  - AWS credentials
  - Knowledge Base IDs (if you want to keep them private)
  - `.env` files
  - Private keys

- **Consider:**
  - Using GitHub Secrets for CI/CD
  - Environment variables for sensitive config
  - Private repository if containing sensitive info

## 📚 Documentation

The repository includes:
- `README.md` - Main documentation
- `KNOWLEDGE_BASE_SETUP.md` - KB setup guide
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - MIT License

All documentation is ready for GitHub!
