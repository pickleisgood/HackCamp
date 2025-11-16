# 🚀 HackCamp - Single Command Reference

## TL;DR

```bash
python3 run.py <GEMINI_KEY> <MAPS_KEY>
```

Done! App runs at http://localhost:3000

---

## Copy-Paste Ready Commands

### macOS / Linux
```bash
python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

### Windows (Command Prompt)
```cmd
python run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

### Windows (PowerShell)
```powershell
python .\run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

---

## URLs After Running

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## Common Tasks

| Task | Command |
|------|---------|
| **Run app** | `python3 run.py <GEMINI_KEY> <MAPS_KEY>` |
| **Stop servers** | `Ctrl+C` |
| **Kill stuck process (macOS)** | `lsof -i :8000 \| awk '{print $2}' \| xargs kill -9` |
| **Kill stuck process (Windows)** | `taskkill /PID <PID> /F` |
| **Check Python** | `python --version` |
| **Check Node.js** | `npm --version` |
| **Got npm error?** | See `WINDOWS_SETUP.md` |

---

## File Purposes

| File | Purpose |
|------|---------|
| `run.py` | **Main startup script - USE THIS** |
| `run.sh` | Bash alternative (macOS/Linux) |
| `run.bat` | Batch alternative (Windows) |
| `START_HERE.md` | Full documentation |
| `QUICKSTART.md` | Quick start guide |
| `SINGLE_COMMAND_SETUP.md` | Implementation details |

---

## First Time?

1. Get API keys:
   - Gemini: https://makersuite.google.com/app/apikey
   - Maps: https://console.cloud.google.com/

2. Run command:
   ```bash
   python3 run.py <GEMINI_KEY> <MAPS_KEY>
   ```

3. Wait 5-10 minutes for dependency installation

4. Open http://localhost:3000

---

## Need Help?

- **Script won't run**: Check Python version (`python3 --version`)
- **Dependencies fail**: Check internet connection
- **Port in use**: Kill process on port 8000 or 3000
- **API key wrong**: Re-run with correct keys
- **See full docs**: Read `START_HERE.md`

---

**That's it! You're ready to go!** 🎉
