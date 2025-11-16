# ✅ Windows Error Fix - "npm not found"

## Problem

User on Windows got this error:
```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

The error occurred when the script tried to run `npm install`.

## Root Cause

**Node.js was not installed on the Windows computer.**

The `npm` command is part of Node.js, so when npm isn't in the PATH, the system can't find it.

## Solution Implemented

### 1. Added Prerequisites Check to `run.py`

The script now:
- ✅ Checks if npm is installed BEFORE trying to use it
- ✅ Checks Python version
- ✅ Shows helpful error messages with installation links
- ✅ Exits gracefully with clear instructions

### 2. Enhanced Error Messages

If npm is not found, the user now sees:
```
✗ npm not found ✗

Prerequisites Not Met

✗ npm is NOT installed

To fix:
1. Install Node.js (includes npm):
   → Download from https://nodejs.org/
   → Choose LTS (Long Term Support) version
   → Run the installer
   → Restart your terminal/PowerShell

After installing, verify with:
  npm --version
```

### 3. Created Windows Setup Guide

New file: `WINDOWS_SETUP.md`
- Step-by-step Node.js installation
- PowerShell tips
- Troubleshooting for Windows
- Copy-paste commands

### 4. Created Troubleshooting Guide

New file: `TROUBLESHOOTING.md`
- Common issues and fixes
- Windows-specific tips
- Command examples
- Getting help section

## Files Updated/Created

| File | Change | Status |
|------|--------|--------|
| `run.py` | Added `check_prerequisites()` function | ✅ Updated |
| `run.py` | Added `check_command_exists()` function | ✅ Updated |
| `run.py` | Enhanced error handling | ✅ Updated |
| `WINDOWS_SETUP.md` | NEW file with step-by-step guide | ✅ Created |
| `TROUBLESHOOTING.md` | NEW file with common issues | ✅ Created |
| `QUICK_REFERENCE.md` | Added reference to Windows guide | ✅ Updated |

## New Behavior

### Before
- Script tried to run npm without checking
- Failed with confusing error
- No helpful message
- User had to figure it out

### After
- Script checks for npm first
- Provides clear error message
- Shows installation link
- Links to Windows guide
- Much clearer path forward

## Testing

To test on Windows:
```powershell
# If npm IS installed, everything works as before
python run.py YOUR_GEMINI_KEY YOUR_MAPS_KEY

# If npm is NOT installed, script shows:
# ✗ npm not found ✗
# ... with helpful instructions ...
```

## For the User

Tell them:

1. **Download Node.js** from https://nodejs.org/ (LTS version)
2. **Run the installer** and restart PowerShell
3. **Run the HackCamp command again**

The script now shows exactly what to do if something is missing!

## Additional Improvements

### Better Error Messages
- Shows which prerequisites are missing
- Links to download pages
- Step-by-step instructions
- Restart reminders (common Windows issue)

### Better Timeout Handling
- Added 5-minute timeout for pip install
- Handles slow internet connections
- Continues gracefully if installation takes a while

### Better Backend Setup
- More robust error handling
- Doesn't fail if dependencies are already installed
- Clear messages about what's happening

## Documentation

Users are now directed to:
1. **WINDOWS_SETUP.md** - For Windows-specific help
2. **TROUBLESHOOTING.md** - For general issues
3. **QUICK_REFERENCE.md** - For quick commands
4. **START_HERE.md** - For complete documentation

---

**Result: Windows users now get clear, actionable error messages instead of confusing technical errors!** ✅
