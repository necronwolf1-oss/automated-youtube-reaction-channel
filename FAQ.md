# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q: I get "ModuleNotFoundError: No module named 'moviepy'"

**A:** You didn't install dependencies. Run:
```bash
pip install -r requirements.txt
```

If it still fails, try:
```bash
pip install --force-reinstall -r requirements.txt
```

---

### Q: "FFmpeg not found" error

**A:** FFmpeg isn't installed or not in PATH.

**Windows:**
```bash
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo dnf install ffmpeg      # Fedora
```

---

### Q: "Config file not found"

**A:** Make sure you're running from the repo root directory:
```bash
cd automated-youtube-reaction-channel
python3 main.py
```

---

## API Keys & Authentication

### Q: "API key not configured" error

**A:** Your `.env` file is missing or empty.

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

---

### Q: "OPENAI_API_KEY" shows as None

**A:** Make sure you're loading .env correctly:
```bash
# After editing .env, restart Python
# Don't just re-run - the environment isn't reloaded

# Test it:
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

---

### Q: How do I get API keys?

**A:**

**OpenAI:**
1. https://platform.openai.com/signup
2. Verify email & phone
3. https://platform.openai.com/account/api-keys
4. Create new key
5. Copy to `.env`

**ElevenLabs:**
1. https://elevenlabs.io/sign-up
2. Go to Account → API Key
3. Copy key to `.env`
4. Go to Voice Library → Select voice → Copy Voice ID to `.env`

---

## Video Processing

### Q: Video rendering is super slow

**A:** Video encoding is CPU-intensive. You can optimize:

```yaml
# In config.yaml - trade quality for speed
video:
  preset: "ultrafast"  # Instead of "medium"
  output_resolution: [1280, 720]  # Smaller resolution
  fps: 24              # Lower FPS
```

Or use GPU acceleration if you have NVIDIA/AMD GPU.

---

### Q: "Out of memory" error during rendering

**A:** Video processing uses a lot of RAM. Solutions:

1. Lower resolution:
```yaml
video:
  output_resolution: [1024, 576]  # Smaller
```

2. Close other programs
3. Increase system RAM
4. Use cloud GPU (Google Colab, AWS)

---

### Q: Output video has no audio

**A:** ElevenLabs voiceover failed. Debug:

```bash
# Check logs
tail -f logs/automation.log

# Test ElevenLabs API
python3 << 'EOF'
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ELEVENLABS_API_KEY')
voice_id = os.getenv('ELEVENLABS_VOICE_ID')

headers = {'xi-api-key': key}
response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers)

if response.status_code == 200:
    print("✓ ElevenLabs API working")
else:
    print(f"✗ Error: {response.status_code} - {response.text}")
EOF
```

---

### Q: Avatar sprite is distorted

**A:** Sprite image might be wrong size or format.

```bash
# Check sprite files
file assets/sprites/image_*.png

# They should be:
# - PNG format
# - Minimum 256x256px
# - Transparent background preferred

# Regenerate or replace sprites
```

---

## Costs & Free Tier

### Q: I ran out of OpenAI credits

**A:** Your $5 free trial is used up. Options:

1. Use cheaper model:
```yaml
openai:
  model: "gpt-3.5-turbo"  # 50x cheaper
```

2. Upgrade account ($5-100/month plans)
3. Use free alternatives (see FREE_TIER_GUIDE.md)

---

### Q: How long does my ElevenLabs free tier last?

**A:** 10,000 characters per month, resets monthly.

```bash
# Check usage
python3 << 'EOF'
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ELEVENLABS_API_KEY')
headers = {'xi-api-key': key}
response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers)
data = response.json()
print(f"Used: {data.get('character_count', 0)} / 10,000")
EOF
```

---

### Q: Can I use this without paying anything?

**A:** Yes! See `FREE_TIER_GUIDE.md` for full details.

- OpenAI: $5 free trial (15-50 videos)
- ElevenLabs: 10,000 chars/month free (10-20 videos)
- Everything else: 100% free

---

## Customization

### Q: How do I use different emotions/expressions?

**A:** Edit `config.yaml` to map emotions to your sprite images:

```yaml
sprites:
  threatening: "assets/sprites/your_image_1.png"
  smirking: "assets/sprites/your_image_2.png"
  # ... etc
```

---

### Q: Can I add more emotions?

**A:** Yes! Edit `config.yaml` and `main.py`:

```yaml
sprites:
  confused: "assets/sprites/confused.png"
  excited: "assets/sprites/excited.png"
```

Then update the script generation prompt to use new emotions.

---

### Q: How do I change the avatar size/position?

**A:** Edit `config.yaml`:

```yaml
avatar:
  height: 500          # Larger sprite
  position: ["center", "bottom"]  # Different position
  audio_reactivity:
    max_scale_factor: 1.15  # More dramatic reactions
```

---

## Troubleshooting

### Q: "Sprite file not found" but files exist

**A:** Check file paths in `config.yaml`:

```bash
# Verify files exist
ls -la assets/sprites/

# Check config paths
grep -r "image_3" config.yaml

# Make sure paths are relative or absolute
# Relative: assets/sprites/image_3.png
# Absolute: /full/path/to/assets/sprites/image_3.png
```

---

### Q: Script generation returns invalid JSON

**A:** OpenAI returned bad format. Debug:

```python
# Check raw response
import requests
import json

# Make a test call manually
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {key}"},
    json=payload
)

print(response.json())  # See actual response
```

Try:
- Simpler prompt
- Lower temperature
- Try GPT-4o instead of 3.5-turbo

---

### Q: "Download failed" - can't get YouTube video

**A:** Video URL invalid or unavailable.

```bash
# Test URL
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# Try different format
yt-dlp --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"

# Update yt-dlp
pip install --upgrade yt-dlp
```

---

### Q: Logs show "ERROR" but video still processes

**A:** Some errors are warnings. Check log level:

```yaml
logging:
  level: "INFO"  # Reduce noise
  # DEBUG - very verbose
  # INFO - normal
  # WARNING - issues only
  # ERROR - problems only
```

---

## Performance & Optimization

### Q: How can I make videos faster?

**A:**

1. Lower resolution
2. Lower FPS (24 instead of 30)
3. Faster codec preset
4. Shorter scripts
5. Smaller sprites

```yaml
video:
  output_resolution: [1024, 576]  # Was 1280x720
  fps: 24                         # Was 30
  preset: "fast"                  # Was "medium"

script:
  default_scene_duration: 3.0  # Was 5.0
```

---

### Q: Can I run multiple videos at once?

**A:** Not recommended (uses too much RAM). But you can batch:

```bash
python3 batch_processor.py --batch examples/batch_example.json
```

This processes videos sequentially.

---

## Advanced Topics

### Q: Can I use local LLM instead of OpenAI?

**A:** Yes! Use Ollama or similar:

```bash
pip install ollama
```

Then modify `main.py` to use local model.

---

### Q: Can I host this on a server/cloud?

**A:** Yes! See `SETUP.md` for Docker setup.

```bash
docker build -t reaction-channel .
docker run -it --env-file .env reaction-channel
```

---

### Q: Can I use GPU for faster rendering?

**A:** Yes! Install FFmpeg with NVIDIA support:

```bash
# Install NVIDIA CUDA libraries first
# Then compile FFmpeg with --enable-cuda-nvcc

# Or use prebuilt: https://developer.nvidia.com/ffmpeg

# Update config:
video:
  codec: "hevc_nvenc"  # NVIDIA GPU encoder
```

---

## Still Need Help?

- **GitHub Issues**: https://github.com/necronwolf1-oss/automated-youtube-reaction-channel/issues
- **Check Logs**: `tail -f logs/automation.log`
- **Review Config**: Make sure `config.yaml` is correct
- **Test Components**: Run test scripts individually

**Happy creating! 🚀**
