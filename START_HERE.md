# 🍽️ HackCamp - AI-Powered Restaurant Finder

Find your perfect restaurant with AI-powered search, advanced filtering, and Google Maps integration.

## 🚀 Quick Start - One Command!

```bash
python3 run.py <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
```

### Example:
```bash
python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

That's it! The script will:
- ✅ Set up both backend and frontend environments
- ✅ Install all dependencies automatically
- ✅ Start FastAPI backend (port 8000)
- ✅ Start React frontend (port 3000)
- ✅ Open the app in your browser

### 🌐 Access the App
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📋 Requirements

Before running, you need:

1. **Python 3.8+** - Download from python.org
2. **Node.js + npm** - Download from nodejs.org
3. **Google Gemini API Key** - Get it from https://makersuite.google.com/app/apikey
4. **Google Maps API Key** - Get it from https://console.cloud.google.com/

---

## ✨ Features

### 🤖 AI-Powered Search
- Uses Google Generative AI (Gemini 2.5 Flash) to find restaurants
- Understands complex natural language queries
- Smart filtering based on your preferences

### 🎯 Smart Filtering
- **Budget Range** - Budget friendly, moderate, upscale, fine dining
- **Dietary Restrictions** - Vegetarian, vegan, gluten-free, kosher, halal
- **Cuisine Types** - Any cuisine preference
- **Minimum Rating** - Filter by star rating
- **Service Types** - Dine-in, takeout, delivery
- **Accessibility** - Wheelchair accessible, etc.
- **Operating Hours** - Open now, extended hours, etc.

### 📍 Google Maps Integration
- View restaurant locations on interactive map
- See pins for each restaurant
- Click for detailed information

### 🎨 Beautiful UI
- Clean, modern interface
- Smooth animations and transitions
- Real-time loading feedback
- Responsive design (mobile-friendly)

### ⚡ Performance
- Real-time search results
- Instant filter updates
- Optimized API calls
- Smooth infinite scroll

---

## 📁 Project Structure

```
HackCamp/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── styles/          # CSS styling
│   │   └── utils/           # Helper functions
│   ├── package.json
│   └── .env                 # Frontend config
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── models/          # Data models
│   │   └── config.py        # Configuration
│   ├── run.py               # Start script
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Backend config
│
├── run.py                   # Master startup script
├── QUICKSTART.md            # Quick start guide
├── IMPLEMENTATION_GUIDE.md  # Detailed implementation
└── README.md                # This file
```

---

## 🛠️ Troubleshooting

### Port Already in Use
If you get "Address already in use" error:

**Find and kill the process:**
```bash
# macOS/Linux
lsof -i :8000        # Find backend process
lsof -i :3000        # Find frontend process
kill -9 <PID>        # Kill the process

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Dependencies Not Installing
Make sure you have:
- Python 3.8+ (`python3 --version`)
- npm 6+ (`npm --version`)
- Internet connection (for downloading packages)

### Backend Not Starting
Check if Uvicorn is installed:
```bash
pip install uvicorn fastapi
```

### Frontend Not Starting
Check if npm dependencies are installed:
```bash
cd frontend
npm install
```

---

## 📖 Documentation

For more detailed information, see:
- **[QUICKSTART.md](./QUICKSTART.md)** - Quick start guide
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Complete implementation details
- **[CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md)** - Summary of all changes

---

## 🎯 How to Use

1. **Start the app**: `python3 run.py <GEMINI_KEY> <MAPS_KEY>`
2. **Enter location**: Type a city or address
3. **Select filters**: Click "🔧 Refine Search" to customize
4. **Search**: Click "🔍 Search" to find restaurants
5. **View results**: See restaurants on map and in list
6. **Scroll**: Infinite scroll to see more results

---

## 🔐 API Keys

### Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### Google Maps API Key
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable "Maps JavaScript API" and "Google Places API"
4. Create an API key
5. Copy the key

---

## 🚫 Stopping the App

Press `Ctrl+C` in the terminal. The script will gracefully shut down both servers.

---

## 📝 License

This project is part of HackCamp. All rights reserved.

---

## 🤝 Support

For issues or questions, check:
1. **QUICKSTART.md** - Quick start guide
2. **IMPLEMENTATION_GUIDE.md** - Detailed guide
3. Terminal output - Check for error messages

---

**Enjoy your perfect restaurant search! 🍽️✨**
