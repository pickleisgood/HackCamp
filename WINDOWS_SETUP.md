# 🪟 Windows Setup Guide

## Quick Fix for "npm not found" Error

**Your computer is missing Node.js (which includes npm).**

### Step 1: Install Node.js

1. **Download Node.js:**
   - Go to https://nodejs.org/
   - Click the big **LTS** (Long Term Support) button
   - Wait for download to finish

2. **Run the Installer:**
   - Double-click the `.msi` file you downloaded
   - Click "Next" through the installation
   - When you see the option, **make sure to check "Automatically install the necessary tools"**
   - Click "Install"
   - Wait for it to finish

3. **Close and Reopen PowerShell:**
   - Close your current PowerShell window
   - Open a NEW PowerShell window

### Step 2: Verify Installation

Open PowerShell and type:
```powershell
npm --version
```

You should see a version number like `10.9.0`.

If you see "command not found", restart your computer and try again.

### Step 3: Run HackCamp

Now run:
```powershell
cd C:\Users\alina\Downloads\HackCamp
python run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

---

## Detailed Step-by-Step

### If You Get "npm not found"

**These are the ONLY things you need to do:**

#### Option A: Using PowerShell (Recommended)

1. Open PowerShell (right-click → "Run as administrator")
2. Run:
   ```powershell
   npm --version
   ```
   - If you see a version number → npm is installed, problem is elsewhere
   - If you see "command not found" → go to next step

3. Install Node.js:
   - Download: https://nodejs.org/
   - Download the **LTS** version
   - Double-click the file
   - Click Next, Next, Next, Install
   - Restart PowerShell

4. Verify again:
   ```powershell
   npm --version
   ```

5. Try the HackCamp command again

#### Option B: Using Command Prompt (cmd.exe)

Same as above, just use cmd.exe instead of PowerShell.

---

## Understanding the Error

```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

This means: **The system can't find the `npm` command**

Why? Because **Node.js is not installed**.

The `npm` command is part of Node.js, so you must install Node.js first.

---

## What Each Tool Does

| Tool | What It Does | Where to Get |
|------|-------------|-------------|
| **Python** | Runs the script | https://www.python.org/ |
| **Node.js** | Runs the React frontend | https://nodejs.org/ |
| **npm** | Installs JavaScript packages | Included with Node.js |

---

## Installation Checklist

Before running the HackCamp command, verify:

- [ ] Python is installed (`python --version` shows 3.8+)
- [ ] Node.js is installed (`npm --version` shows a number)
- [ ] PowerShell/cmd can find both commands
- [ ] You've restarted PowerShell after installing anything new
- [ ] You have both API keys ready

---

## PowerShell Tips

### Running as Administrator

1. Search for "PowerShell"
2. Right-click "Windows PowerShell"
3. Select "Run as administrator"
4. Click "Yes"

### Navigating to Your Folder

```powershell
# Go to Downloads (example)
cd C:\Users\alina\Downloads\HackCamp

# List files to verify you're in the right place
ls

# You should see run.py in the list
```

### If PowerShell Won't Run the Script

Try adding `python`:
```powershell
python .\run.py YOUR_KEY1 YOUR_KEY2
```

Or use the full path:
```powershell
python C:\Users\alina\Downloads\HackCamp\run.py YOUR_KEY1 YOUR_KEY2
```

---

## Troubleshooting Checklist

| Problem | Solution |
|---------|----------|
| "npm not found" | Install Node.js from https://nodejs.org/ |
| "python not found" | Install Python from https://www.python.org/ |
| "Port already in use" | Run `taskkill /PID 12345 /F` (see TROUBLESHOOTING.md) |
| "Permission denied" | Run PowerShell as Administrator (right-click → Run as admin) |
| Slow on first run | Normal! Takes 5-10 min, later runs are 30 sec |
| Still doesn't work | Check TROUBLESHOOTING.md or START_HERE.md |

---

## After Installing Node.js

### Important: Restart PowerShell

After installing Node.js, you **must** close and reopen PowerShell for it to recognize the new command.

**Don't skip this step!**

---

## The Complete Setup (Windows)

1. **Install Node.js**
   - Download from https://nodejs.org/ (LTS)
   - Run the installer
   - Restart PowerShell

2. **Verify Node.js**
   ```powershell
   npm --version
   node --version
   ```

3. **Navigate to HackCamp**
   ```powershell
   cd C:\Users\alina\Downloads\HackCamp
   ```

4. **Run HackCamp**
   ```powershell
   python run.py YOUR_GEMINI_KEY YOUR_MAPS_KEY
   ```

5. **Wait 5-10 minutes** for first-time setup

6. **Access at** http://localhost:3000

---

**That's it! Once Node.js is installed, everything else is automatic.** ✅
