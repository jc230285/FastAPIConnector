# FastAPIConnector

A FastAPI microservice that acts as a connector between OCR (PaddleOCR) and LLM (Ollama) services for document processing.

## Features

- **Parse Receipts**: Upload an image and extract structured data (vendor, date, invoice number, line items, total)
- **Summarize Documents**: Provide text and get a summary with topic tags

## Deployment

### Prerequisites

- Docker and Docker Compose installed
- Sufficient resources for running LLM models (e.g., Mistral-7B requires ~4GB VRAM)

### Build the Connector Image

Build the connector Docker image locally:

```bash
docker build -t fastapi-connector:latest .
```

### Quick Start

1. Build the connector image (see above)
2. Run the services:

```bash
docker-compose up
```

This will start:
- OpenWebUI on port 5000
- Ollama on port 11434
- PaddleOCR on port 8866
- Connector API on port 8000

### Pull LLM Model

After starting, pull the required model:

```bash
docker-compose exec ollama ollama pull mistral:7b-instruct-q4_0
```

## API Usage

### Parse Receipt

Upload an image file to extract receipt data:

```bash
curl -X POST "http://localhost:8000/parse-receipt" \
     -F "file=@receipt.jpg"
```

### Summarize Document

Send text for summarization:

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your document text here"}'
```

## Integration with n8n

Use the connector API endpoints in your n8n workflows for document processing automation.

## Configuration

Environment variables for the connector:

- `OCR_URL`: URL of the OCR service (default: http://paddleocr:8866)
- `LLM_API`: URL of the LLM API (default: http://ollama:11434)

## 🚀 Coolify Deployment

This project is ready for one-click deployment on Coolify!

### Quick Deploy

1. **Run the finalizer script:**
   ```bash
   ./finalize-for-coolify.sh
   ```

2. **Import the stack in Coolify:**
   - Go to your Coolify dashboard
   - Create a new project or select existing
   - Choose "Import" → "From YAML"
   - Upload or paste the contents of `coolify-stack.yml`
   - Replace `yourdomain.com` with your actual domain
   - Deploy!

### Services Included

| Service | URL Pattern | Description |
|---------|-------------|-------------|
| **FastAPIConnector** | `https://connector.yourdomain.com` | Your OCR→LLM orchestration API |
| **OpenWebUI** | `https://ai.yourdomain.com` | Web UI for chatting with models |
| **Ollama** | `https://ollama.yourdomain.com` | Local LLM runtime |
| **PaddleOCR** | `https://ocr.yourdomain.com` | OCR service for documents |

### Post-Deployment Setup

1. **Load models in Ollama:**
   ```bash
   curl https://ollama.yourdomain.com/api/pull -d '{"name": "mistral:7b-instruct-q4_0"}'
   ```

2. **Test the connector:**
   ```bash
   curl -X POST https://connector.yourdomain.com/parse-receipt \
     -F "file=@receipt.jpg"
   ```

3. **Access OpenWebUI:**
   - Visit `https://ai.yourdomain.com`
   - Models will auto-appear after loading in Ollama

### Manual Build (Alternative)

If you prefer manual setup:

```bash
# Build locally
docker build -t fastapi-connector:latest .

# Test locally
docker run -p 8000:8000 --env-file .env fastapi-connector:latest
```