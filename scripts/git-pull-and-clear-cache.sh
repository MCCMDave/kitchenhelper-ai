#!/bin/bash
# Git Pull + Cloudflare Cache Clear
# Complete deployment automation for Kitchen project

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}  Kitchen Deployment - Auto Update${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""

# Step 1: Git Pull
echo -e "${YELLOW}📥 Step 1/3: Pulling latest changes from GitHub...${NC}"
cd /home/pi/kitchenhelper-ai || exit 1

git fetch origin
CHANGES=$(git log HEAD..origin/main --oneline)

if [ -z "$CHANGES" ]; then
    echo -e "${GREEN}✅ Already up to date!${NC}"
    echo ""
    exit 0
fi

echo -e "${BLUE}Changes to be pulled:${NC}"
echo "$CHANGES"
echo ""

git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Git pull successful${NC}"
else
    echo -e "${RED}❌ Git pull failed${NC}"
    exit 1
fi

echo ""

# Step 2: Clean Python cache
echo -e "${YELLOW}🧹 Step 2/3: Cleaning Python cache...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✅ Cache cleaned${NC}"
echo ""

# Step 3: Clear Cloudflare cache
echo -e "${YELLOW}☁️  Step 3/3: Clearing Cloudflare cache...${NC}"

if [ -z "$CLOUDFLARE_ZONE_ID" ] || [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  Cloudflare credentials not set - skipping cache clear${NC}"
    echo -e "${YELLOW}💡 Set CLOUDFLARE_ZONE_ID and CLOUDFLARE_API_TOKEN to enable${NC}"
    echo ""
else
    RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
         -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
         -H "Content-Type: application/json" \
         --data '{"purge_everything":true}')

    if echo "$RESPONSE" | grep -q '"success":true'; then
        echo -e "${GREEN}✅ Cloudflare cache cleared!${NC}"
    else
        echo -e "${RED}❌ Failed to clear Cloudflare cache${NC}"
        echo "Response: $RESPONSE"
    fi
    echo ""
fi

# Summary
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Changes visible on:${NC}"
echo "  • ${BLUE}IP:Port${NC}     → http://192.168.2.54:8081 (immediate)"
echo "  • ${BLUE}Domain${NC}      → https://kitchen.kitchenhelper-ai.de (10-30s)"
echo "  • ${BLUE}Root${NC}        → https://kitchenhelper-ai.de (10-30s)"
echo ""
echo -e "${YELLOW}💡 Tip: Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)${NC}"
