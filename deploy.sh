#!/bin/bash
# ============================================
# KitchenHelper-AI Deployment Script
# For Raspberry Pi (Linux/ARM64)
# ============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  KitchenHelper-AI Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root is not recommended${NC}"
fi

# Navigate to project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "\n${YELLOW}[1/5] Pulling latest changes from git...${NC}"
git pull origin main

echo -e "\n${YELLOW}[2/5] Checking for .env file...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi
echo -e "${GREEN}✓ .env file found${NC}"

echo -e "\n${YELLOW}[3/5] Building Docker image...${NC}"
docker compose build --no-cache

echo -e "\n${YELLOW}[4/5] Stopping existing containers...${NC}"
docker compose down || true

echo -e "\n${YELLOW}[5/5] Starting new containers...${NC}"
docker compose up -d

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

# Show status
echo -e "\n${YELLOW}Container Status:${NC}"
docker compose ps

echo -e "\n${YELLOW}Health Check:${NC}"
sleep 5  # Wait for container to start
curl -s http://localhost:8000/health || echo -e "${RED}Health check failed - container may still be starting${NC}"

echo -e "\n\n${GREEN}API:${NC} http://localhost:8000"
echo -e "${GREEN}Docs:${NC} http://localhost:8000/docs"
echo -e "\n${YELLOW}View logs:${NC} docker compose logs -f"
