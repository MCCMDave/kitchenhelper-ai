#!/bin/bash
# Cloudflare Cache Clear Script
# Automatically clears Cloudflare cache after git pull
# Free API - No cost!

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔄 Cloudflare Cache Clear Script${NC}"
echo ""

# Check if CLOUDFLARE_ZONE_ID and CLOUDFLARE_API_TOKEN are set
if [ -z "$CLOUDFLARE_ZONE_ID" ] || [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo -e "${RED}❌ Error: CLOUDFLARE_ZONE_ID or CLOUDFLARE_API_TOKEN not set${NC}"
    echo ""
    echo "Please set environment variables:"
    echo "  export CLOUDFLARE_ZONE_ID='your_zone_id'"
    echo "  export CLOUDFLARE_API_TOKEN='your_api_token'"
    echo ""
    echo "Get them from:"
    echo "  1. Zone ID: Cloudflare Dashboard → Your Domain → Overview (right sidebar)"
    echo "  2. API Token: Cloudflare Dashboard → My Profile → API Tokens → Create Token"
    echo "     Template: 'Edit Zone DNS' or create custom with 'Zone.Cache Purge'"
    echo ""
    exit 1
fi

# Purge entire cache
echo -e "${YELLOW}🧹 Purging Cloudflare cache...${NC}"

RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
     -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
     -H "Content-Type: application/json" \
     --data '{"purge_everything":true}')

# Check if successful
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ Cache cleared successfully!${NC}"
    echo ""
    echo -e "${GREEN}Changes are now visible on:${NC}"
    echo "  • https://kitchenhelper-ai.de"
    echo "  • https://kitchen.kitchenhelper-ai.de"
    echo ""
else
    echo -e "${RED}❌ Failed to clear cache${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

echo -e "${YELLOW}💡 Tip: Wait 10-30 seconds, then refresh browser (Ctrl+Shift+R)${NC}"
