#!/bin/bash

echo "========================================"
echo "AI Case Processing Service Setup"
echo "========================================"

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
else
    echo ".env already exists"
fi

# Create .env.docker if not exists
if [ ! -f ".env.docker" ]; then
    echo "Creating .env.docker from .env.docker.example..."
    cp .env.docker.example .env.docker
else
    echo ".env.docker already exists"
fi

echo ""
echo "========================================"
echo "SETUP COMPLETE"
echo "========================================"
echo ""
echo "IMPORTANT:"
echo "Edit .env.docker and set your GROQ_API_KEY"
echo ""
echo "Then run:"
echo ""
echo "docker compose up --build"
echo ""
echo "Swagger UI will be available at:"
echo ""
echo "http://127.0.0.1:8000/docs"
echo ""
