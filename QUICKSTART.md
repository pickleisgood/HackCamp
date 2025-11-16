# 🚀 Quick Start Guide - HackCamp

Run the entire HackCamp application with **a single command**!

## One Command to Run Everything

```bash
python3 run.py <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
```

## Example

```bash
python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

## What the Script Does

The startup script automatically:

1. ✅ **Creates backend environment** - Sets up `.env` file with your API keys
2. ✅ **Installs Python dependencies** - Installs all required packages
3. ✅ **Starts FastAPI backend** - Runs on `http://localhost:8000`
4. ✅ **Creates frontend environment** - Sets up `.env` file with your API keys
5. ✅ **Installs npm dependencies** - Installs all frontend packages
6. ✅ **Starts React frontend** - Runs on `http://localhost:3000`
7. ✅ **Waits for both servers** - Ensures both are ready before continuing
8. ✅ **Displays success message** - Shows all URLs and instructions

## Access the Application

Once the script completes, you'll see:

```
============================================================
🎉 HackCamp is Running!
============================================================

Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs
```

**Open your browser to `http://localhost:3000`** and start using the app!

## Stopping the Application

Press `Ctrl+C` in the terminal running the script. The script will gracefully shut down both servers.

## API Keys

You need two API keys:

1. **Google Gemini API Key** - For AI-powered restaurant search
   - Get it from: https://makersuite.google.com/app/apikey

2. **Google Maps API Key** - For displaying restaurant locations
   - Get it from: https://console.cloud.google.com/

## Troubleshooting

### Port Already in Use
If you get an error like "Address already in use":

**macOS/Linux:**
```bash
# Find process using port 8000 (backend)
lsof -i :8000

# Find process using port 3000 (frontend)
lsof -i :3000

# Kill the process (replace PID with the actual process ID)
kill -9 <PID>
```

**Windows:**
```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Python Not Found
Make sure you have Python 3 installed:
```bash
python3 --version
```

### npm Not Found
Make sure you have Node.js installed:
```bash
npm --version
```

## First Time Running?

On first run, the script will:
- Install ~40 Python packages (takes ~1-2 minutes)
- Install ~1300 npm packages (takes ~2-3 minutes)

**Total first-run time: 5-10 minutes**

Subsequent runs are **much faster** (30 seconds) since dependencies are cached.

## Features Ready to Use

✨ **AI-Powered Restaurant Discovery**
- Enter location and filters
- Gemini AI searches for matching restaurants
- Clear budget labels (not ambiguous symbols)
- Beautiful filter overlay

🔄 **Smart Filtering**
- Budget range
- Dietary restrictions
- Cuisine types
- Minimum rating
- Service types (dine-in, takeout, delivery)
- Accessibility features
- Operating hours

📍 **Google Maps Integration**
- View restaurants on map
- See pins for each location
- Click pins for details

⚡ **Real-time Feedback**
- Loading popup shows AI is searching
- User cannot interact while AI works
- Smooth animations and transitions

---

**That's it! One command, two API keys, and your restaurant finder is running.** 🎉
