#!/usr/bin/env python3
"""
HackCamp - Restaurant Finder Master Startup Script
Usage: python3 run.py <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
Example: python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
"""

import sys
import os
import subprocess
import time
import signal
import platform
from pathlib import Path

# Color codes for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

# Global variables for process cleanup
backend_proc = None
frontend_proc = None

def print_header(text):
    print(f"{BLUE}{'═' * 60}{NC}")
    print(f"{BLUE}{text}{NC}")
    print(f"{BLUE}{'═' * 60}{NC}")

def print_success(text):
    print(f"{GREEN}✓ {text}{NC}")

def print_error(text):
    print(f"{RED}✗ {text}{NC}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{NC}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{NC}")

def check_command_exists(command):
    """Check if a command exists in PATH"""
    result = subprocess.run(
        ["which" if os.name != "nt" else "where", command],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global backend_proc, frontend_proc
    print_info("Shutting down servers...")
    if backend_proc:
        backend_proc.terminate()
    if frontend_proc:
        frontend_proc.terminate()
    
    # Wait for processes to finish
    if backend_proc:
        backend_proc.wait()
    if frontend_proc:
        frontend_proc.wait()
    
    print_success("Servers stopped")
    sys.exit(0)

def check_command_exists(command):
    """Check if a command exists in PATH"""
    result = subprocess.run(
        ["which" if os.name != "nt" else "where", command],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def check_arguments():
    if len(sys.argv) != 3:
        print_header("HackCamp - Restaurant Finder")
        print()
        print_error("Missing API keys!")
        print()
        print("Usage: python3 run.py <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>")
        print()
        print("Example:")
        print("  python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs")
        print()
        sys.exit(1)
    
    return sys.argv[1], sys.argv[2]

def install_nodejs():
    """Install Node.js if not present"""
    print_header("Installing Node.js")
    
    system = platform.system()
    print_info(f"Detected OS: {system}")
    
    if system == "Darwin":  # macOS
        print_info("Installing Node.js via Homebrew...")
        try:
            # Check if Homebrew is installed
            result = subprocess.run(["brew", "--version"], capture_output=True)
            if result.returncode != 0:
                print_error("Homebrew not found. Please install from https://brew.sh")
                return False
            
            subprocess.run(["brew", "install", "node"], check=True)
            print_success("Node.js installed successfully")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install Node.js via Homebrew")
            return False
    
    elif system == "Linux":
        print_info("Installing Node.js via package manager...")
        try:
            # Try apt (Ubuntu/Debian)
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"], check=True, capture_output=True)
            print_success("Node.js installed successfully")
            return True
        except subprocess.CalledProcessError:
            try:
                # Try yum (RedHat/CentOS)
                subprocess.run(["sudo", "yum", "install", "-y", "nodejs", "npm"], check=True, capture_output=True)
                print_success("Node.js installed successfully")
                return True
            except subprocess.CalledProcessError:
                print_error("Failed to install Node.js. Please install manually from https://nodejs.org")
                return False
    
    elif system == "Windows":
        print_warning("Automatic Node.js installation not supported on Windows")
        print_info("Please download and install Node.js from https://nodejs.org/")
        print_info("Make sure to add Node.js to PATH during installation")
        print_info("After installation, restart this script")
        return False
    
    return False

def check_prerequisites():
    """Check if all required tools are installed"""
    print_header("Checking Prerequisites")
    
    issues = []
    
    # Check Python
    print_info(f"Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required (you have {})".format(sys.version.split()[0]))
    else:
        print_success("Python 3.8+ ✓")
    
    # Check npm
    if check_command_exists("npm"):
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            npm_version = result.stdout.strip()
            print_success(f"npm {npm_version} ✓")
        except:
            issues.append("npm found but cannot determine version")
    else:
        print_error("npm not found ✗")
        print_info("Attempting to install Node.js...")
        if not install_nodejs():
            issues.append("npm is NOT installed - please install Node.js manually")
        else:
            # Retry check
            if check_command_exists("npm"):
                try:
                    result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
                    npm_version = result.stdout.strip()
                    print_success(f"npm {npm_version} ✓")
                except:
                    issues.append("npm found but cannot verify")
            else:
                issues.append("npm installation failed")
    
    # Check git (optional but useful)
    if check_command_exists("git"):
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            git_version = result.stdout.strip()
            print_success(f"{git_version} ✓")
        except:
            pass
    
    # If there are critical issues, show instructions and exit
    if issues:
        print()
        print_header("Prerequisites Not Met")
        print()
        for issue in issues:
            print_error(issue)
        print()
        print("To fix:")
        print()
        if "npm" in str(issues):
            print("1. Install Node.js (includes npm):")
            print("   → Download from https://nodejs.org/")
            print("   → Choose LTS (Long Term Support) version")
            print("   → Run the installer")
            print("   → Restart your terminal/PowerShell")
            print()
        if "Python" in str(issues):
            print("2. Install Python 3.8+:")
            print("   → Download from https://www.python.org/")
            print("   → Run the installer")
            print("   → Restart your terminal/PowerShell")
            print()
        print("After installing, verify with:")
        print("  python --version")
        print("  npm --version")
        print()
        sys.exit(1)
    
    print()
    print_success("All prerequisites met! ✓")

def setup_backend(script_dir, gemini_key, maps_key):
    print_header("Setting up Backend")
    
    backend_dir = Path(script_dir) / "backend"
    os.chdir(backend_dir)
    
    # Create .env file
    print_info("Configuring backend environment variables...")
    env_content = f"""GOOGLE_MAPS_API_KEY={maps_key}
GEMINI_API_KEY={gemini_key}
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print_success("Backend .env file created")
    
    # Install requirements using system Python
    print_info("Installing Python dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
            check=True,
            capture_output=False,
            text=True,
            timeout=300
        )
        print_success("Python dependencies installed")
    except subprocess.TimeoutExpired:
        print_error("Dependency installation timed out (5+ minutes)")
        print_info("Attempting to continue...")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install Python dependencies")
        print_info("Attempting to continue (dependencies might already be installed)...")
    except Exception as e:
        print_error(f"Error installing dependencies: {e}")
        print_info("Attempting to continue...")

def setup_frontend(script_dir, maps_key):
    print_header("Setting up Frontend")
    
    # Check if npm is installed
    if not check_command_exists("npm"):
        print_error("npm is not installed or not in PATH!")
        print()
        print("To fix this:")
        print("1. Download Node.js from https://nodejs.org/")
        print("2. Install it (includes npm)")
        print("3. Restart your terminal/PowerShell")
        print("4. Run this script again")
        print()
        print("After installation, verify with: npm --version")
        sys.exit(1)
    
    frontend_dir = Path(script_dir) / "frontend"
    os.chdir(frontend_dir)
    
    # Create .env file
    print_info("Configuring frontend environment variables...")
    env_content = f"""REACT_APP_GOOGLE_MAPS_API_KEY={maps_key}
REACT_APP_BACKEND_URL=http://localhost:8000
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print_success("Frontend .env file created")
    
    # Check if node_modules exists
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print_info("Installing npm dependencies (this may take a few minutes)...")
        try:
            subprocess.run(["npm", "install"], check=True, capture_output=False)
            print_success("npm dependencies installed")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install npm dependencies: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print_error("npm command not found!")
            print("Please install Node.js from https://nodejs.org/")
            sys.exit(1)
    else:
        print_success("npm dependencies already installed")

def wait_for_port(port, timeout=30):
    """Wait for a service to be available on a port"""
    import socket
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', port))
            sock.close()
            return True
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.5)
    
    return False

def main():
    global backend_proc, frontend_proc
    
    gemini_key, maps_key = check_arguments()
    
    # Get script directory
    script_dir = Path(__file__).parent.resolve()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_header("🚀 HackCamp - Restaurant Finder Starting")
    print()
    
    # Check prerequisites FIRST
    check_prerequisites()
    print()
    
    # Setup backend
    setup_backend(str(script_dir), gemini_key, maps_key)
    
    # Start backend
    print_info("Starting FastAPI backend server on http://localhost:8000...")
    backend_dir = Path(script_dir) / "backend"
    backend_proc = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=str(backend_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print_success("Backend server started")
    
    # Wait for backend to be ready
    print_info("Waiting for backend to be ready...")
    if wait_for_port(8000):
        print_success("Backend is ready!")
    else:
        print_error("Backend failed to start within timeout")
        backend_proc.terminate()
        sys.exit(1)
    
    # Setup frontend
    setup_frontend(str(script_dir), maps_key)
    
    # Start frontend
    print_info("Starting React frontend server on http://localhost:3000...")
    frontend_dir = Path(script_dir) / "frontend"
    env = os.environ.copy()
    env["BROWSER"] = "none"
    frontend_proc = subprocess.Popen(
        ["npm", "start"],
        cwd=str(frontend_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print_success("Frontend server started")
    
    # Wait for frontend to be ready
    print_info("Waiting for frontend to be ready...")
    if wait_for_port(3000):
        print_success("Frontend is ready!")
    else:
        print_error("Frontend failed to start within timeout")
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(1)
    
    # Success!
    print_header("🎉 HackCamp is Running!")
    print()
    print(f"{GREEN}Frontend:{NC} {BLUE}http://localhost:3000{NC}")
    print(f"{GREEN}Backend:{NC}  {BLUE}http://localhost:8000{NC}")
    print(f"{GREEN}API Docs:{NC} {BLUE}http://localhost:8000/docs{NC}")
    print()
    print(f"{YELLOW}Press Ctrl+C to stop both servers{NC}")
    print()
    
    try:
        # Wait for both processes
        while True:
            if backend_proc and backend_proc.poll() is not None:
                print_error("Backend process exited")
                signal_handler(None, None)
            if frontend_proc and frontend_proc.poll() is not None:
                print_error("Frontend process exited")
                signal_handler(None, None)
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
