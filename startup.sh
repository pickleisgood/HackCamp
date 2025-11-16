#!/bin/bash
# Quick startup script for the Restaurant Finder project

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Restaurant Finder - Project Startup${NC}"
echo "========================================"

# Get the project directory
PROJECT_DIR="/Users/andrexue/GitHub/HackCamp"

# Check if both directories exist
if [ ! -d "$PROJECT_DIR/backend" ] || [ ! -d "$PROJECT_DIR/frontend" ]; then
    echo -e "${RED}❌ Error: Project directories not found${NC}"
    exit 1
fi

# Check if Python dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing backend dependencies...${NC}"
    cd "$PROJECT_DIR/backend"
    python3 -m pip install -r requirements.txt
fi

# Check if Node dependencies are installed
if [ ! -d "$PROJECT_DIR/frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Installing frontend dependencies...${NC}"
    cd "$PROJECT_DIR/frontend"
    npm install
fi

echo ""
echo -e "${GREEN}✅ All dependencies verified!${NC}"
echo ""
echo -e "${BLUE}To run the project, open TWO terminals and run:${NC}"
echo ""
echo -e "${GREEN}Terminal 1 (Backend):${NC}"
echo -e "  cd $PROJECT_DIR/backend && python3 run.py"
echo ""
echo -e "${GREEN}Terminal 2 (Frontend):${NC}"
echo -e "  cd $PROJECT_DIR/frontend && npm start"
echo ""
echo -e "${BLUE}Access the application at:${NC}"
echo -e "  🖥️  Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "  📚 API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  ❤️  Health: ${GREEN}http://localhost:8000/health${NC}"
echo ""
