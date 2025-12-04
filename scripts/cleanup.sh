#!/bin/bash
# Cleanup Script - Remove unnecessary files
# Safe to run anytime

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🧹 Kitchen Cleanup Script${NC}"
echo ""

CLEANED=0

# 1. Python cache files
echo -e "${YELLOW}Removing Python cache files...${NC}"
PYCACHE=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*.pyd" -delete 2>/dev/null || true
echo -e "${GREEN}✅ Removed $PYCACHE __pycache__ directories${NC}"
CLEANED=$((CLEANED + PYCACHE))

# 2. OS files
echo -e "${YELLOW}Removing OS junk files...${NC}"
OS_FILES=$(find . -type f \( -name ".DS_Store" -o -name "Thumbs.db" -o -name "desktop.ini" \) 2>/dev/null | wc -l)
find . -type f \( -name ".DS_Store" -o -name "Thumbs.db" -o -name "desktop.ini" \) -delete 2>/dev/null || true
echo -e "${GREEN}✅ Removed $OS_FILES OS files${NC}"
CLEANED=$((CLEANED + OS_FILES))

# 3. Log files (keep newest)
echo -e "${YELLOW}Removing old log files...${NC}"
LOG_FILES=$(find backend/logs -type f -name "*.log" -mtime +7 2>/dev/null | wc -l)
find backend/logs -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
echo -e "${GREEN}✅ Removed $LOG_FILES old log files (>7 days)${NC}"
CLEANED=$((CLEANED + LOG_FILES))

# 4. Pytest cache
echo -e "${YELLOW}Removing test cache...${NC}"
PYTEST=$(find . -type d -name ".pytest_cache" 2>/dev/null | wc -l)
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name ".coverage" -delete 2>/dev/null || true
echo -e "${GREEN}✅ Removed $PYTEST test cache directories${NC}"
CLEANED=$((CLEANED + PYTEST))

# 5. Editor temp files
echo -e "${YELLOW}Removing editor temp files...${NC}"
TEMP=$(find . -type f \( -name "*.swp" -o -name "*.swo" -o -name "*~" \) 2>/dev/null | wc -l)
find . -type f \( -name "*.swp" -o -name "*.swo" -o -name "*~" \) -delete 2>/dev/null || true
echo -e "${GREEN}✅ Removed $TEMP editor temp files${NC}"
CLEANED=$((CLEANED + TEMP))

# Summary
echo ""
if [ $CLEANED -gt 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Cleanup complete! Removed $CLEANED items${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
else
    echo -e "${GREEN}✅ Nothing to clean - project already tidy!${NC}"
fi

echo ""
echo -e "${YELLOW}💡 Run this script regularly to keep project clean${NC}"
