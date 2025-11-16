# 🪟 Windows Setup Guide - Fixed!

## The Issue You Encountered

```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

This happened because **Node.js/npm was not installed** on your computer.

---

## ✅ What Changed

The `run.py` script now:
- ✅ **Checks for Node.js first**
- ✅ **Shows clear error if missing**
- ✅ **Provides download link**
- ✅ **Gives step-by-step instructions**
- ✅ **Guides you to restart terminal**

---

## 🚀 For Windows Users - Fix the Error

### Step 1: Download Node.js

1. Go to https://nodejs.org/
2. Click "LTS" (Long Term Support) - **NOT** "Current"
3. Download the Windows installer
4. Run the installer

### Step 2: Install Node.js

During installation, **IMPORTANT:**
- ✅ Accept the license
- ✅ Keep default installation path
- ✅ **CHECK "Add to PATH"** ← Very important!
- ✅ Check "Install npm"
- ✅ Click "Install"
- ✅ Wait for installation to complete

### Step 3: Restart PowerShell/Command Prompt

**Close and reopen PowerShell or Command Prompt** (this is important!)

### Step 4: Verify Installation

Open PowerShell/Command Prompt and run:

```powershell
node --version
npm --version
```

You should see version numbers like:
```
v20.0.0
10.0.0
```

### Step 5: Run HackCamp

Now run the command:

```powershell
python run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

Or with your own API keys:

```powershell
python run.py <GEMINI_KEY> <MAPS_KEY>
```

---

## ✅ Expected Output

After running the command, you should see:

```
═══════════════════════════════════════════════════════════
🚀 HackCamp - Restaurant Finder Starting
═══════════════════════════════════════════════════════════

ℹ Checking Prerequisites
✓ Python 3.11 ✓
✓ npm 11.6.0 ✓
✓ All prerequisites met! ✓

ℹ Setting up Backend
✓ Backend .env file created
ℹ Installing Python dependencies...
✓ Python dependencies installed
ℹ Starting FastAPI backend server on http://localhost:8000...
✓ Backend server started
✓ Backend is ready!

ℹ Setting up Frontend
✓ Frontend .env file created
ℹ Installing npm dependencies (this may take a few minutes)...
✓ npm dependencies installed
ℹ Starting React frontend server on http://localhost:3000...
✓ Frontend server started
✓ Frontend is ready!

═══════════════════════════════════════════════════════════
🎉 HackCamp is Running!
═══════════════════════════════════════════════════════════

Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs

Press Ctrl+C to stop both servers
```

---

## 🌐 Access Your App

Open your web browser and go to:

```
http://localhost:3000
```

You should see the HackCamp Restaurant Finder interface!

---

## ❌ Still Getting Error?

### If npm still not found:

1. **Right-click PowerShell** → "Run as Administrator"
2. Run: `npm --version`
3. If still not found, Node.js wasn't properly installed

**To reinstall:**
1. Download from https://nodejs.org/ again
2. **Uninstall old version first** (Windows Settings → Apps)
3. Restart computer
4. Install fresh
5. **CHECK "Add to PATH"**
6. Restart terminal

### If Python error:

Make sure you have Python 3.8+ installed:
```powershell
python --version
```

If not, download from https://www.python.org/

---

## 🎯 Quick Checklist

- ✅ Downloaded Node.js LTS from nodejs.org
- ✅ Installed with "Add to PATH" checked
- ✅ Restarted PowerShell/Command Prompt
- ✅ Verified: `npm --version` works
- ✅ Verified: `python --version` works
- ✅ Run: `python run.py <KEY1> <KEY2>`
- ✅ Go to: http://localhost:3000

---

## 💡 Tips

- **Always use PowerShell or Command Prompt** (not other terminals)
- **"Add to PATH"** is crucial - don't skip it!
- **Restart terminal** after installing Node.js
- **Use Python 3.8+** for best compatibility
- **Copy-paste commands** to avoid typos

---

## 🆘 Still Need Help?

See these documents:
- `DEPENDENCIES_GUIDE.md` - Full dependency guide
- `AUTO_DEPENDENCY_INSTALLATION.md` - Technical details
- `QUICK_REFERENCE.md` - Quick commands

---

## 🎉 You're All Set!

Once Node.js is installed and the script runs successfully, your HackCamp restaurant finder will be running at:

```
http://localhost:3000
```

Enjoy! 🍽️✨
