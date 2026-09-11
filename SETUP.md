# Complete Setup Guide - Automated YouTube Reaction Channel

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [API Key Configuration](#api-key-configuration)
4. [Asset Preparation](#asset-preparation)
5. [Testing & Verification](#testing--verification)
6. [Docker Setup (Optional)](#docker-setup-optional)

---

## System Requirements

### Hardware
- **CPU**: Intel i5/AMD Ryzen 5 or better (video encoding is CPU-intensive)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ free space (for temp files and output videos)
- **GPU** (Optional): NVIDIA/AMD for faster video encoding

### Software
- **Python**: 3.8 or higher
- **FFmpeg**: Required for moviepy
- **Git**: For cloning repository

### Operating System Support
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 18.04+, Debian, Fedora, etc.)

---

## Step-by-Step Installation

### 1. Install System Dependencies

#### Windows
```powershell
# Using Chocolatey (if installed)
choco install python ffmpeg git

# Or manually download from:
# - Python: https://www.python.org/downloads/
# - FFmpeg: https://ffmpeg.org/download.html
# - Git: https://git-scm.com/download/win
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11 ffmpeg git

# Or using MacPorts
sudo port install python311 ffmpeg git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip ffmpeg git
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install -y python3.11 python3-pip ffmpeg git
```

### 2. Clone Repository

```bash
# Clone the repo
git clone https://github.com/necronwolf1-oss/automated-youtube-reaction-channel.git
cd automated-youtube-reaction-channel

# Verify directory structure
ls -la
# Should show: main.py, config.py, logger_setup.py, config.yaml, requirements.txt, etc.
```

### 3. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv
# On macOS/Linux:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# Verify activation (should show (venv) in prompt)
which python  # macOS/Linux
where python  # Windows
```

### 4. Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep -E "moviepy|yt-dlp|openai|elevenlabs"
```

---

## API Key Configuration

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in (requires paid account)
3. Click "Create new secret key"
4. Copy the key (you can only see it once!)
5. Store it safely

**Pricing**: ~$0.03-0.15 per 5 minute video depending on script length

### Step 2: Get ElevenLabs API Key

1. Go to https://elevenlabs.io
2. Sign up or log in (free tier available)
3. Go to Account → API Key
4. Copy your API key
5. Go to Voice Library → Select a voice
6. Copy the Voice ID (looks like: `21m00Tcm4TlvDq8ikWAM`)

**Pricing**: Free tier includes 10,000 characters/month (enough for ~1-2 videos)

### Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit with your editor of choice
nano .env          # Linux/macOS
# or
notepad .env       # Windows
```

Fill in `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

### Step 4: Verify Configuration

```bash
# Test that config loads correctly
python3 -c "from config import get_config; c = get_config(); print('✓ Config loaded successfully')"

# Should output: ✓ Config loaded successfully
```

---

## Asset Preparation

### Creating or Finding Sprites

You need 7 PNG sprite images (PNGTuber avatars) for different emotions:

**Option A: Generate with AI**
1. Use Midjourney, DALL-E 3, or Stable Diffusion
2. Prompt example: `"cute anime character with wolf ears, transparent background, PNG"`
3. Generate 7 variants for each emotion

**Option B: Use Existing Character Assets**
- Browse https://opengameart.org/
- Search DeviantArt for "PNGTuber assets"
- Commission an artist on Fiverr/Upwork

**Option C: Simplify (For Testing)**
- Use same image for all emotions temporarily
- Test pipeline before full implementation

### Setting Up Sprite Directory

```bash
# Create sprites directory
mkdir -p assets/sprites

# Download or copy your PNG files into this directory
# Files should be:
# - PNG format
# - Transparent background preferred
# - Minimum 256x256px
# - Named: image_3.png, image_4.png, image_5.png, image_6.png, image_7.png, image_8.png, image_9.png

# Verify sprites
ls -lh assets/sprites/
```

### Update config.yaml (if needed)

If sprites are in different location, update `config.yaml`:

```yaml
sprites:
  threatening: "assets/sprites/image_3.png"
  smirking: "assets/sprites/image_4.png"
  mischievous: "assets/sprites/image_5.png"
  hyped: "assets/sprites/image_6.png"
  playful: "assets/sprites/image_7.png"
  heart_eyes: "assets/sprites/image_8.png"
  star_eyes: "assets/sprites/image_9.png"
```

---

## Testing & Verification

### Test 1: Verify Dependencies

```bash
# Activate venv first
source venv/bin/activate

# Run import test
python3 -c "
import os
print('✓ Python', os.sys.version)
import moviepy; print('✓ moviepy', moviepy.__version__)
import yt_dlp; print('✓ yt_dlp installed')
import requests; print('✓ requests installed')
import numpy; print('✓ numpy installed')
from config import get_config; print('✓ config working')
from logger_setup import get_logger; print('✓ logging working')
"
```

### Test 2: Verify FFmpeg

```bash
# Check FFmpeg is installed and accessible
ffmpeg -version | head -n 1

# Output should be: ffmpeg version X.X.X...
```

### Test 3: Verify API Keys

```bash
# Test OpenAI connection
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')
try:
    response = openai.Model.list()
    print('✓ OpenAI API key is valid')
except Exception as e:
    print(f'✗ OpenAI API key invalid: {e}')
"

# Test ElevenLabs connection
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
import requests

key = os.getenv('ELEVENLABS_API_KEY')
headers = {'xi-api-key': key}
response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers)
if response.status_code == 200:
    print('✓ ElevenLabs API key is valid')
else:
    print(f'✗ ElevenLabs API key invalid: {response.text}')
"
```

### Test 4: Verify Sprites

```bash
# Check all sprites exist
python3 -c "
from config import get_config
from pathlib import Path

config = get_config()
print('Checking sprites:')
for emotion, path in config.sprites.items():
    exists = Path(path).exists()
    status = '✓' if exists else '✗'
    print(f'{status} {emotion}: {path}')
"
```

### Test 5: Dry Run (No API Calls)

```bash
# Test logging and config
python3 -c "
from logger_setup import get_logger
from config import get_config

logger = get_logger()
config = get_config()

logger.info('===== System Check =====')
logger.info(f'OpenAI Model: {config.openai.model}')
logger.info(f'Video Resolution: {config.video.output_resolution}')
logger.info(f'Avatar Height: {config.avatar.height}')
logger.info(f'Logging Level: {config.logging.level}')
logger.info('✓ All systems ready')
"
```

### Test 6: Generate Test Script

```bash
# This tests OpenAI without downloading/compositing video
python3 << 'EOF'
from config import get_config
from logger_setup import get_logger
from main import generate_channel_script
import json

logger = get_logger()
config = get_config()

try:
    script = generate_channel_script(
        topic="Test reaction",
        video_title="Test Video",
        config=config
    )
    logger.info("✓ Script generation successful!")
    logger.info(f"Generated {len(script.get('scenes', []))} scenes")
except Exception as e:
    logger.error(f"✗ Script generation failed: {e}", exc_info=True)
EOF
```

### Test 7: Generate Test Voiceover

```bash
# This tests ElevenLabs without video processing
python3 << 'EOF'
from config import get_config
from logger_setup import get_logger
from main import generate_voiceover
from pathlib import Path

logger = get_logger()
config = get_config()

try:
    test_audio = ".temp/test_audio.mp3"
    Path(".temp").mkdir(exist_ok=True)
    
    generate_voiceover(
        text="This is a test voiceover for the automated reaction channel!",
        filename=test_audio,
        config=config
    )
    logger.info("✓ Voiceover generation successful!")
    
    import os
    size = os.path.getsize(test_audio) / 1024
    logger.info(f"Audio file size: {size:.1f}KB")
except Exception as e:
    logger.error(f"✗ Voiceover generation failed: {e}", exc_info=True)
EOF
```

---

## Full Pipeline Test

Once all individual tests pass, run the full pipeline:

```bash
# Activate venv
source venv/bin/activate

# Run with a SHORT test video
python3 main.py

# This will:
# 1. Download source video (~30 seconds)
# 2. Generate script via OpenAI
# 3. Generate voiceovers via ElevenLabs
# 4. Create avatar clips
# 5. Render output video
# Takes 5-15 minutes depending on video length
```

Monitor the logs:
```bash
# In another terminal, watch logs in real-time
tail -f logs/automation.log
```

---

## Docker Setup (Optional)

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p assets/sprites logs .temp

# Run application
CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  reaction-generator:
    build: .
    volumes:
      - ./assets/sprites:/app/assets/sprites
      - ./logs:/app/logs
      - ./.env:/app/.env
    environment:
      - PYTHONUNBUFFERED=1
    stdin_open: true
    tty: true
```

### Using Docker

```bash
# Build image
docker build -t reaction-channel .

# Run container
docker run -it --env-file .env -v $(pwd)/assets/sprites:/app/assets/sprites -v $(pwd)/logs:/app/logs reaction-channel

# Or with docker-compose
docker-compose up --build
```

---

## Troubleshooting Setup Issues

### "ModuleNotFoundError: No module named 'moviepy'"
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Or manually
pip install moviepy==1.0.3
```

### "FFmpeg not found"
```bash
# Check FFmpeg is in PATH
which ffmpeg  # macOS/Linux
where ffmpeg  # Windows

# If not found, reinstall FFmpeg or add to PATH
```

### "Config file not found"
```bash
# Ensure you're running from repo root
pwd  # Should end with: automated-youtube-reaction-channel

# Verify config.yaml exists
ls -la config.yaml
```

### "API key invalid"
```bash
# Verify .env file is NOT in .gitignore'd location
cat .env | grep OPENAI_API_KEY

# Check key format (should start with sk-proj- for OpenAI)
# Regenerate key if needed on platform websites
```

### "Sprite files not found"
```bash
# Verify directory and files
ls -la assets/sprites/

# Should show 7 PNG files:
# image_3.png, image_4.png, image_5.png, image_6.png, image_7.png, image_8.png, image_9.png

# Check file permissions
chmod 644 assets/sprites/*.png
```

---

## Next Steps After Setup

1. **Customize Configuration** - Edit `config.yaml` for your preferences
2. **Create Sprites** - Generate or find PNGTuber assets
3. **Test Pipeline** - Run with a test YouTube URL
4. **Batch Processing** - Create scripts for multiple videos
5. **Deploy** - Set up on server or cloud platform

---

## Getting Help

- **GitHub Issues**: https://github.com/necronwolf1-oss/automated-youtube-reaction-channel/issues
- **Logs**: Check `logs/automation.log` for detailed errors
- **Config Issues**: Review `config.yaml` syntax and file paths
- **API Issues**: Verify keys on OpenAI and ElevenLabs dashboards

