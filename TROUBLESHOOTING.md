# ❌ Common Issues & Fixes

## Issue: "The system cannot find the file specified" (npm not found)

### What This Means
Node.js or npm is not installed on your computer.

### How to Fix

**Step 1: Install Node.js**
1. Go to https://nodejs.org/
2. Download the **LTS (Long Term Support)** version
3. Run the installer
4. Follow the installation steps
5. **Important**: Restart your terminal/PowerShell after installation

**Step 2: Verify Installation**
Open a new PowerShell or Command Prompt and run:
```powershell
npm --version
node --version
```

You should see version numbers like:
```
10.9.0
v20.11.0
```

**Step 3: Run the Script Again**
```powershell
python run.py YOUR_GEMINI_KEY YOUR_MAPS_KEY
```

---

## Issue: "The system cannot find the file specified" (Python not found)

### How to Fix

**Step 1: Install Python**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or newer
3. Run the installer
4. **IMPORTANT**: Check "Add python.exe to PATH"
5. Click Install
6. Restart your terminal/PowerShell

**Step 2: Verify Installation**
```powershell
python --version
```

You should see something like: `Python 3.11.0`

---

## Issue: Port Already in Use

### Error Message
```
Address already in use
Port 8000 or 3000 already in use
```

### How to Fix

**Find and stop the process using the port:**

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Find process using port 3000
netstat -ano | findstr :3000
```

You'll see output like:
```
TCP    127.0.0.1:8000    0.0.0.0:0    LISTENING    12345
```

The last number (12345) is the Process ID. Kill it with:

```powershell
taskkill /PID 12345 /F
```

Then try running the script again.

---

## Issue: Permission Denied or Access Denied

### How to Fix

**Run PowerShell as Administrator:**
1. Search for "PowerShell"
2. Right-click "Windows PowerShell"
3. Select "Run as administrator"
4. Click "Yes"
5. Then run the command

---

## Issue: API Keys Not Working

### Error Message
```
Invalid API key
Authentication failed
```

### How to Fix

1. **Check your keys are correct:**
   - Gemini key: https://makersuite.google.com/app/apikey
   - Maps key: https://console.cloud.google.com/

2. **Make sure keys are enabled:**
   - Gemini: Enable the API in your Google account
   - Maps: Enable all required APIs (Maps JavaScript API, Places API)

3. **Check for typos:**
   - Copy and paste directly from Google
   - Don't add extra spaces
   - They usually start with "AIza..."

---

## Issue: Dependencies Installation Fails

### How to Fix

**Try installing manually:**

**For Python (backend):**
```powershell
cd backend
pip install -r requirements.txt
```

**For Node.js (frontend):**
```powershell
cd frontend
npm install
```

If these work, the script should also work.

---

## Issue: Slow Installation on First Run

### What This Means
This is normal! First run takes 5-10 minutes because it's:
- Installing ~40 Python packages
- Installing ~1300 npm packages
- Compiling everything

### Solution
Just wait! Later runs will be much faster (~30 seconds).

---

## Issue: "The system cannot find the path specified"

### How to Fix

1. Make sure you're in the correct directory:
   ```powershell
   cd C:\Users\alina\Downloads\HackCamp
   ```

2. Verify the `run.py` file exists:
   ```powershell
   ls run.py
   ```

3. Then run:
   ```powershell
   python run.py YOUR_GEMINI_KEY YOUR_MAPS_KEY
   ```

---

## Issue: Frontend Shows Blank Page

### How to Fix

1. Check browser console for errors (F12)
2. Make sure backend is running (check http://localhost:8000/docs)
3. Verify API keys in `.env` files:
   - `backend/.env`
   - `frontend/.env`
4. Restart both servers

---

## Getting Help

If you still have issues:

1. **Check the error message** - Most errors are clear about what's wrong
2. **Read the output** - The script shows where it fails
3. **Check prerequisites** - Run with check:
   ```powershell
   python run.py
   ```
   (without keys) to see what's missing

4. **See documentation:**
   - `START_HERE.md` - Complete guide
   - `QUICK_REFERENCE.md` - Quick commands
   - `DOCUMENTATION_INDEX.md` - All docs

---

## Windows-Specific Tips

### Using Command Prompt (cmd.exe) vs PowerShell

Both work, but **PowerShell is recommended**:
```powershell
# PowerShell
python run.py KEY1 KEY2
```

### Long File Paths

Windows has a 260-character path limit. If you get path errors:
1. Move the project to a shorter path
2. Or enable long paths (admin required)

### Backslashes in Commands

Windows uses `\` for paths, Python uses `/`. Usually handles automatically, but if issues:
```powershell
# This works on Windows too
python .\run.py KEY1 KEY2
```

---

**Most common issue: Node.js not installed. Just download and install it!** ✅
