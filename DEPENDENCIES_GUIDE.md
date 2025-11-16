# 🛠️ HackCamp - Automatic Dependency Installation

The `run.py` script now **automatically handles all dependencies**, including Node.js installation!

## What Gets Installed

### ✅ Automatically Handled
- ✓ Python packages (fastapi, uvicorn, pydantic, google-generativeai, etc.)
- ✓ npm packages (React, Axios, Google Maps, etc.)
- ✓ Node.js (if missing on macOS/Linux)

### ⚠️ May Require Manual Action (Windows)
- Node.js on Windows (automated installers exist but require admin)

---

## 🚀 Single Command Does Everything

```bash
python3 run.py <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
```

The script will:

1. **Check Prerequisites**
   - Verify Python 3.8+
   - Check for npm/Node.js
   - Auto-install Node.js on macOS/Linux if missing
   - Show clear instructions if anything is missing

2. **Install Backend Dependencies**
   - ~40 Python packages from `requirements.txt`
   - Includes: FastAPI, Uvicorn, Pydantic, Google APIs, etc.

3. **Install Frontend Dependencies**
   - ~1300 npm packages from `package.json`
   - Includes: React, Axios, Google Maps, etc.

4. **Start Both Servers**
   - FastAPI backend (port 8000)
   - React frontend (port 3000)

---

## 📋 What's Installed

### Backend Python Dependencies
```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pydantic>=2.0.0           # Data validation
python-dotenv==1.0.0      # Environment variables
google-generativeai>=0.5.0 # Gemini AI
googlemaps>=4.0.0         # Google Maps API
httpx>=0.25.0             # HTTP client
requests>=2.31.0          # HTTP library
python-multipart>=0.0.6   # File uploads
```

### Frontend npm Dependencies
```
react                       # UI framework
react-dom                   # React DOM
axios                       # HTTP client
@react-google-maps/api      # Google Maps
react-infinite-scroll       # Infinite scroll
react-router-dom            # Routing
```

### System Requirements
```
Python 3.8+                 # Programming language
Node.js 14+                 # JavaScript runtime (includes npm)
npm 6+                      # Package manager
```

---

## 🖥️ Platform-Specific Installation

### macOS
**Node.js Installation (if missing):**
```bash
# Script auto-installs via Homebrew
# If not installed, you'll see instructions
brew install node
```

### Linux (Ubuntu/Debian)
**Node.js Installation (if missing):**
```bash
# Script auto-installs via apt
sudo apt update
sudo apt install nodejs npm
```

### Linux (RedHat/CentOS)
**Node.js Installation (if missing):**
```bash
# Script auto-installs via yum
sudo yum install nodejs npm
```

### Windows
**Node.js Installation:**
1. Script will show error if npm not found
2. Download from https://nodejs.org/ (LTS version)
3. Run installer (includes npm)
4. Make sure "Add to PATH" is checked ✓
5. Restart PowerShell/Command Prompt
6. Re-run the script

---

## ✅ Verification Before Running

The script checks for:

| Component | Status | If Missing |
|-----------|--------|-----------|
| Python 3.8+ | ✓ Required | Shows error with link |
| npm/Node.js | ✓ Required | Auto-install (macOS/Linux) |
| Git | Optional | Not required |

---

## 🚨 Troubleshooting

### Error: "npm not found" on Windows

**Solution:**
1. Download Node.js from https://nodejs.org/
2. Choose LTS (Long Term Support)
3. Run installer
4. **Important:** Check "Add to PATH" during install
5. Restart PowerShell/Command Prompt
6. Verify: `npm --version`
7. Re-run the script

### Error: "Permission denied" on macOS/Linux

**Solution:**
```bash
# Make script executable
chmod +x run.py

# Try running again
python3 run.py <GEMINI_KEY> <MAPS_KEY>
```

### Error: "pip install failed"

**Solution:**
- Check internet connection
- Try manually: `pip install -r backend/requirements.txt`
- If persistent, check Python version: `python3 --version`

### Error: "npm install failed"

**Solution:**
- Check internet connection
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules`: `rm -rf frontend/node_modules`
- Re-run the script

### Error: "Homebrew not found" on macOS

**Solution:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then re-run HackCamp script
python3 run.py <GEMINI_KEY> <MAPS_KEY>
```

---

## 📊 Installation Times

| Step | Time | Notes |
|------|------|-------|
| Prerequisites check | ~10 sec | Checks for tools |
| Node.js install (if needed) | ~2-5 min | macOS/Linux only |
| Python deps install | ~1-2 min | 40 packages |
| npm deps install | ~2-3 min | 1300 packages |
| Total (first run) | 5-10 min | All automated |
| Subsequent runs | ~30 sec | Deps cached |

---

## 🎯 What Each Step Does

### 1. Check Prerequisites
```
✓ Python 3.8+
✓ npm/Node.js
✓ Git (optional)
```

If missing, script offers to install or shows manual instructions.

### 2. Setup Backend
```
✓ Create backend/.env with API keys
✓ Install 40+ Python packages
✓ Verify installation
```

### 3. Setup Frontend
```
✓ Create frontend/.env with API keys
✓ Install 1300+ npm packages
✓ Verify installation
```

### 4. Start Servers
```
✓ Start FastAPI backend (port 8000)
✓ Start React frontend (port 3000)
✓ Wait for both to be ready
✓ Show success message
```

---

## 🔧 Manual Installation (if needed)

If the script doesn't work, you can install manually:

### Backend
```bash
cd backend
pip install -r requirements.txt
python3 run.py
```

### Frontend (new terminal)
```bash
cd frontend
npm install
npm start
```

---

## 📝 Requirements Files

### backend/requirements.txt
All Python dependencies listed here. Install with:
```bash
pip install -r backend/requirements.txt
```

### frontend/package.json
All npm dependencies listed here. Install with:
```bash
npm install
```

---

## ✨ Summary

**The `run.py` script automates everything:**
- ✓ Checks system requirements
- ✓ Installs missing tools (Node.js on macOS/Linux)
- ✓ Installs all Python packages
- ✓ Installs all npm packages
- ✓ Configures environment variables
- ✓ Starts both servers
- ✓ Provides helpful error messages

**No manual installation needed!** Just run:

```bash
python3 run.py <GEMINI_KEY> <MAPS_KEY>
```

---

**Everything is handled automatically!** 🎉
