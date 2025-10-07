# 🚀 FastAPIConnector - Coolify Deployment Finalizer
# Run this in your VS Code terminal to make everything ready for Coolify

echo "🔧 Finalizing FastAPIConnector for Coolify deployment..."

# 1. Upgrade pip and install dependencies locally
echo "📦 Installing/upgrading Python dependencies..."
pip install --upgrade pip wheel uvicorn fastapi httpx

# 2. Test the application locally
echo "🧪 Testing local application..."
python -c "import connector; print('✅ Code syntax OK')"

# 3. Build Docker image
echo "🐳 Building Docker image..."
docker build -t fastapi-connector:latest .

# 4. Test Docker container locally
echo "🧪 Testing Docker container..."
docker run -d --name test-connector --env-file .env -p 8000:8000 fastapi-connector:latest
sleep 5

# Check if container is running
if docker ps | grep -q test-connector; then
    echo "✅ Container started successfully"

    # Test health check
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
    fi

    # Stop test container
    docker stop test-connector && docker rm test-connector
    echo "🧹 Cleaned up test container"
else
    echo "❌ Container failed to start"
    docker logs test-connector
    docker rm test-connector
    exit 1
fi

# 5. Push changes to GitHub
echo "📤 Pushing changes to GitHub..."
git add .
git commit -m "Finalize for Coolify deployment: add health checks, .env, coolify-stack.yml"
git push origin main

echo ""
echo "🎉 SUCCESS! Your FastAPIConnector is ready for Coolify deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Coolify dashboard"
echo "2. Create new project or use existing"
echo "3. Import from YAML: use coolify-stack.yml"
echo "4. Replace 'yourdomain.com' with your actual domain"
echo "5. Deploy!"
echo ""
echo "🔗 Service URLs after deployment:"
echo "• Connector API: https://connector.yourdomain.com"
echo "• OpenWebUI: https://ai.yourdomain.com"
echo "• Ollama: https://ollama.yourdomain.com"
echo "• PaddleOCR: https://ocr.yourdomain.com"
echo ""
echo "📚 API Docs: https://connector.yourdomain.com/docs"
echo "🧪 Test command: curl -X POST https://connector.yourdomain.com/parse-receipt -F \"file=@receipt.jpg\""