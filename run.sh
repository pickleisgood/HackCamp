#!/bin/bash

#############################################################################
# HackCamp - Restaurant Finder Master Startup Script
# Usage: ./run.sh <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
# Example: ./run.sh your_gemini_api_key your_google_maps_api_key
#############################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if both arguments are provided
if [ $# -ne 2 ]; then
    print_header "HackCamp - Restaurant Finder"
    echo ""
    print_error "Missing API keys!"
    echo ""
    echo "Usage: ./run.sh <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>"
    echo ""
    echo "Example:"
    echo "  ./run.sh your_gemini_api_key your_google_maps_api_key"
    echo ""
    exit 1
fi

GEMINI_KEY=$1
MAPS_KEY=$2

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

print_header "🚀 HackCamp - Restaurant Finder Starting"

# Function to cleanup on exit
cleanup() {
    print_info "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    print_success "Servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# ============================================================================
# BACKEND SETUP
# ============================================================================

print_header "Setting up Backend"

BACKEND_DIR="$SCRIPT_DIR/backend"
cd "$BACKEND_DIR"

# Create .env file
print_info "Configuring backend environment variables..."
cat > .env << EOF
GOOGLE_MAPS_API_KEY=$MAPS_KEY
GEMINI_API_KEY=$GEMINI_KEY
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
EOF
print_success "Backend .env file created"

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Check if requirements are installed
if [ ! -f "venv/bin/uvicorn" ]; then
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    print_success "Python dependencies installed"
else
    print_success "Python dependencies already installed"
fi

# Start backend server
print_info "Starting FastAPI backend server on http://localhost:8000..."
$SCRIPT_DIR/backend/venv/bin/python3 run.py &
BACKEND_PID=$!
print_success "Backend server started (PID: $BACKEND_PID)"

# Wait for backend to be ready
print_info "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        print_success "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Backend failed to start"
        kill $BACKEND_PID
        exit 1
    fi
    sleep 1
done

# ============================================================================
# FRONTEND SETUP
# ============================================================================

print_header "Setting up Frontend"

FRONTEND_DIR="$SCRIPT_DIR/frontend"
cd "$FRONTEND_DIR"

# Create .env file
print_info "Configuring frontend environment variables..."
cat > .env << EOF
REACT_APP_GOOGLE_MAPS_API_KEY=$MAPS_KEY
REACT_APP_BACKEND_URL=http://localhost:8000
EOF
print_success "Frontend .env file created"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies (this may take a few minutes)..."
    npm install > /dev/null 2>&1
    print_success "npm dependencies installed"
else
    print_success "npm dependencies already installed"
fi

# Start frontend server
print_info "Starting React frontend server on http://localhost:3000..."
BROWSER=none SKIP_PREFLIGHT_CHECK=true NODE_OPTIONS="--no-warnings --localstorage-file=/tmp/localstorage.json" npm start &
FRONTEND_PID=$!
print_success "Frontend server started (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
print_info "Waiting for frontend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Frontend failed to start"
        kill $BACKEND_PID $FRONTEND_PID
        exit 1
    fi
    sleep 1
done

# ============================================================================
# SUCCESS
# ============================================================================

print_header "🎉 HackCamp is Running!"

echo ""
echo -e "${GREEN}Frontend:${NC} ${BLUE}http://localhost:3000${NC}"
echo -e "${GREEN}Backend:${NC}  ${BLUE}http://localhost:8000${NC}"
echo -e "${GREEN}API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""

# Keep the script running
wait
