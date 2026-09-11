# Quick Command Reference

## Installation & Setup

```bash
# First time setup
git clone https://github.com/necronwolf1-oss/automated-youtube-reaction-channel.git
cd automated-youtube-reaction-channel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Add sprites
mkdir -p assets/sprites
# Copy image_3.png through image_9.png here
```

## Running Videos

```bash
# Activate virtual environment
source venv/bin/activate

# Check system setup
python3 quickstart.py

# Generate single reaction
python3 run.py "https://www.youtube.com/watch?v=VIDEO_ID" --topic "My reaction topic"

# Generate with custom output
python3 run.py "https://www.youtube.com/watch?v=VIDEO_ID" --output my_video.mp4

# Process batch of videos
python3 run.py --batch examples/batch_example.json

# Just test API keys
python3 run.py --check
```

## Batch Processing

```bash
# Create template
python3 batch_processor.py --template

# Edit batch_template.json with your URLs and topics
# Then run:
python3 batch_processor.py --batch batch_template.json

# Dry run (no processing)
python3 batch_processor.py --batch batch_template.json --dry-run
```

## Script Generation Styles

```bash
# View available prompt templates
python3 examples/prompt_templates.py

# See specific style
python3 examples/prompt_templates.py comedy
python3 examples/prompt_templates.py horror
python3 examples/prompt_templates.py educational
python3 examples/prompt_templates.py analytical
```

## Configuration

```bash
# Edit main config
nano config.yaml

# Use example configs
cat examples/example_config_advanced.yaml

# Verify config
python3 -c "from config import get_config; c = get_config(); print('✓ Config valid')"
```

## Debugging & Logs

```bash
# Watch logs in real-time
tail -f logs/automation.log

# View last 50 lines
tail -50 logs/automation.log

# Search logs
grep "ERROR" logs/automation.log

# Check API usage
python3 << 'EOF'
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ELEVENLABS_API_KEY')
headers = {'xi-api-key': key}
response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers)
data = response.json()
print(f"ElevenLabs - {data.get('character_count', 0)} / 10,000 characters used")
EOF
```

## File Management

```bash
# View generated videos
ls -lh *.mp4

# View temp files
ls -la .temp/

# Clean temp files
rm -rf .temp/*

# View example topics
cat examples/example_topics.txt

# View FAQ
less FAQ.md
```

## Cost Monitoring

```bash
# Check remaining OpenAI credits
# Go to: https://platform.openai.com/account/usage/overview

# Check ElevenLabs character usage
python3 monitor_costs.py

# Estimate cost of batch
python3 batch_processor.py --batch examples/batch_example.json --dry-run
```

## Advanced Options

```bash
# Use faster processing (lower quality)
# Edit config.yaml and set:
# video.preset: ultrafast
# video.output_resolution: [1024, 576]

# Use higher quality (slower processing)
# video.preset: slow
# video.output_resolution: [1920, 1080]
# openai.model: gpt-4o

# Enable debug logging
# Edit config.yaml and set:
# logging.level: DEBUG

# Use different ElevenLabs voice
# Edit .env:
# ELEVENLABS_VOICE_ID=different_voice_id
```

## Troubleshooting Commands

```bash
# Test FFmpeg
ffmpeg -version

# Test Python version
python3 --version

# Test imports
python3 -c "import moviepy; import yt_dlp; import openai; print('✓ All imports work')"

# Test config loading
python3 -c "from config import get_config; c = get_config(); print('✓ Config OK')"

# Test logging
python3 -c "from logger_setup import get_logger; l = get_logger(); l.info('✓ Logging OK')"

# Full system check
python3 quickstart.py
```

## Docker Commands

```bash
# Build image
docker build -t reaction-channel .

# Run container
docker run -it --env-file .env -v $(pwd)/assets/sprites:/app/assets/sprites -v $(pwd)/logs:/app/logs reaction-channel

# Using docker-compose
docker-compose up --build
```

## Common Issues & Fixes

```bash
# "No module named moviepy"
pip install -r requirements.txt

# "FFmpeg not found"
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
# Windows: choco install ffmpeg

# "API key invalid"
# Edit .env file
# Verify keys on OpenAI and ElevenLabs websites

# "Sprite file not found"
# Check: ls -la assets/sprites/
# Verify paths in config.yaml match actual files

# "Out of memory"
# Lower video resolution in config.yaml
# Close other programs

# "Download failed"
# pip install --upgrade yt-dlp
# Try different YouTube URL
```

## Getting Help

```bash
# View README
cat README.md

# View setup guide
cat SETUP.md

# View free tier guide
cat FREE_TIER_GUIDE.md

# View FAQ
cat FAQ.md

# View example topics
cat examples/example_topics.txt

# GitHub issues
open https://github.com/necronwolf1-oss/automated-youtube-reaction-channel/issues
```
