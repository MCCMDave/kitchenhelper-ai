#!/bin/bash
# Complete Deployment Workflow
# Usage: ./scripts/deploy-to-pi.sh "commit message"

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}  Kitchen Complete Deployment Workflow${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""

# Check if commit message provided
COMMIT_MSG="${1:-Update}"

# Step 1: Git Commit & Push
echo -e "${YELLOW}📝 Step 1/5: Git commit & push...${NC}"
git add -A
git commit -m "$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>" || echo "Nothing to commit"

git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Git push failed${NC}"
    exit 1
fi
echo ""

# Step 2: SSH to Pi and pull
echo -e "${YELLOW}📥 Step 2/5: Pulling on Pi...${NC}"
ssh pi "cd /home/dave/kitchenhelper-ai && git pull origin main"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pulled on Pi${NC}"
else
    echo -e "${RED}❌ Git pull on Pi failed${NC}"
    exit 1
fi
echo ""

# Step 3: Restart Frontend
echo -e "${YELLOW}🔄 Step 3/5: Restarting Frontend (HTTP server)...${NC}"
ssh pi "pkill -f 'python3.*8081' && cd /home/dave/kitchenhelper-ai/frontend && nohup python3 -m http.server 8081 --bind 0.0.0.0 > /dev/null 2>&1 &"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend restarted (port 8081)${NC}"
else
    echo -e "${RED}❌ Frontend restart failed${NC}"
fi
echo ""

# Step 4: Restart Backend
echo -e "${YELLOW}🔄 Step 4/5: Restarting Backend (Docker)...${NC}"
ssh pi "cd /home/dave/kitchenhelper-ai && docker-compose restart"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend restarted (Docker)${NC}"
else
    echo -e "${RED}❌ Backend restart failed${NC}"
fi
echo ""

# Step 5: Clear Cloudflare Cache (if configured)
echo -e "${YELLOW}☁️  Step 5/5: Clearing Cloudflare cache...${NC}"

if [ -n "$CLOUDFLARE_ZONE_ID" ] && [ -n "$CLOUDFLARE_API_TOKEN" ]; then
    RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
         -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
         -H "Content-Type: application/json" \
         --data '{"purge_everything":true}')

    if echo "$RESPONSE" | grep -q '"success":true'; then
        echo -e "${GREEN}✅ Cloudflare cache cleared!${NC}"
    else
        echo -e "${RED}❌ Cloudflare cache clear failed${NC}"
        echo "Response: $RESPONSE"
    fi
else
    echo -e "${YELLOW}⚠️  Cloudflare credentials not set - skipping${NC}"
    echo -e "${YELLOW}💡 Set CLOUDFLARE_ZONE_ID and CLOUDFLARE_API_TOKEN to enable${NC}"
    echo -e "${YELLOW}💡 See: CLOUDFLARE-CACHE-SETUP.md${NC}"
fi
echo ""

# Summary
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Your changes are now live:${NC}"
echo "  • ${BLUE}IP:Port${NC}     → http://192.168.2.54:8081 (immediate)"
echo "  • ${BLUE}Domain${NC}      → https://kitchen.kitchenhelper-ai.de"
echo "  • ${BLUE}Landing${NC}     → https://kitchen.kitchenhelper-ai.de/landing.html"
echo ""

if [ -z "$CLOUDFLARE_ZONE_ID" ] || [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo -e "${YELLOW}💡 Note: Domain may take 5-30 min (Cloudflare cache)${NC}"
    echo -e "${YELLOW}   To see changes immediately, set up Cloudflare credentials${NC}"
    echo -e "${YELLOW}   See: CLOUDFLARE-CACHE-SETUP.md${NC}"
else
    echo -e "${GREEN}💡 Domain updated immediately (cache cleared)${NC}"
fi

echo ""
echo -e "${YELLOW}💡 Hard refresh browser: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)${NC}"
