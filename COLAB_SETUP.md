# How to Run on Google Colab from iPhone 📱

Google Colab is the easiest way to run this tool from ANY device (iPhone, Android, laptop, tablet).

## Quick Start (2 minutes)

### Step 1: Open Colab
Click this link directly from your iPhone:
```
https://colab.research.google.com/github/necronwolf1-oss/automated-youtube-reaction-channel/blob/main/colab_simple.py
```

Or go to https://colab.research.google.com and click "GitHub" tab, then paste:
```
necronwolf1-oss/automated-youtube-reaction-channel
```

### Step 2: Copy & Paste Code

Copy this entire code and paste into a new Colab cell:

```python
# ============================================================
# AUTOMATED YOUTUBE REACTION CHANNEL - COLAB VERSION
# ============================================================

print("Installing dependencies...")
!pip install -q moviepy yt-dlp openai elevenlabs pydantic python-dotenv colorama pillow
!apt-get install -y ffmpeg > /dev/null 2>&1
print("✓ Dependencies installed\n")

# Step 1: Get API Keys
import os
from getpass import getpass

print("Enter your API keys (won't display as you type):\n")
openai_key = getpass("OpenAI API Key (sk-...): ")
elevenlabs_key = getpass("ElevenLabs API Key: ")
voice_id = input("ElevenLabs Voice ID: ")

os.environ['OPENAI_API_KEY'] = openai_key
os.environ['ELEVENLABS_API_KEY'] = elevenlabs_key
os.environ['ELEVENLABS_VOICE_ID'] = voice_id

print("\n✓ API keys configured\n")

# Step 2: Clone Repository
!git clone https://github.com/necronwolf1-oss/automated-youtube-reaction-channel.git > /dev/null 2>&1
os.chdir('automated-youtube-reaction-channel')
print("✓ Repository cloned\n")

# Step 3: Create .env file
env_content = f"""OPENAI_API_KEY={openai_key}
ELEVENLABS_API_KEY={elevenlabs_key}
ELEVENLABS_VOICE_ID={voice_id}
"""

with open('.env', 'w') as f:
    f.write(env_content)

print("✓ Configuration file created\n")

# Step 4: Create sprite placeholders
from PIL import Image, ImageDraw
from pathlib import Path

sprite_dir = Path('assets/sprites')
sprite_dir.mkdir(parents=True, exist_ok=True)

emotions = {
    'image_3.png': ('Threatening', (200, 50, 50)),
    'image_4.png': ('Smirking', (200, 150, 50)),
    'image_5.png': ('Mischievous', (200, 200, 50)),
    'image_6.png': ('Hyped', (100, 200, 50)),
    'image_7.png': ('Playful', (50, 200, 200)),
    'image_8.png': ('Heart Eyes', (200, 100, 150)),
    'image_9.png': ('Star Eyes', (150, 100, 200)),
}

for filename, (emotion, color) in emotions.items():
    img = Image.new('RGB', (300, 300), color=color)
    draw = ImageDraw.Draw(img)
    draw.text((80, 135), emotion, fill='white')
    img.save(sprite_dir / filename)

print(f"✓ Created {len(emotions)} sprite placeholders\n")

# Step 5: Test setup
print("Testing configuration...")
from config import get_config
config = get_config()
print(f"✓ Model: {config.openai.model}")
print(f"✓ Resolution: {config.video.output_resolution}")
print(f"✓ All systems ready!\n")

# Step 6: Generate Video
print("="*60)
print("READY TO GENERATE VIDEO")
print("="*60)

# EDIT THESE:
YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Change this!
REACTION_TOPIC = "Reacting to awesome content"  # Change this!

print(f"\nURL: {YOUTUBE_URL}")
print(f"Topic: {REACTION_TOPIC}")
print("\nGenerating video (10-20 minutes)...\n")

from main import build_full_automation_video

try:
    build_full_automation_video(
        media_url=YOUTUBE_URL,
        topic=REACTION_TOPIC
    )
    print("\n✓ VIDEO COMPLETE!")
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("Check your API keys and internet connection")

# Step 7: Download video
print("\n" + "="*60)
print("DOWNLOADING VIDEO")
print("="*60)

from google.colab import files
from pathlib import Path

mp4_files = list(Path('.').glob('*.mp4'))
if mp4_files:
    print(f"\nFound {len(mp4_files)} video(s):")
    for f in mp4_files:
        size = f.stat().st_size / (1024*1024)
        print(f"  - {f.name} ({size:.1f} MB)")
    
    print("\nDownloading...")
    for f in mp4_files:
        files.download(str(f))
        print(f"✓ Downloaded: {f.name}")
else:
    print("No videos found")
```

### Step 3: Edit & Run

1. Change the YouTube URL to your video
2. Change the REACTION_TOPIC to your topic
3. Click the ▶ play button to run
4. Wait 10-20 minutes
5. Click download when finished

## Video Tutorial (for iPhone)

```
1. Open link in Safari: https://colab.research.google.com
2. Paste code above into a cell
3. Change YouTube URL to yours
4. Click play button (▶)
5. Watch video generate live
6. Click download when done
7. Video saves to iPhone Files app or Downloads
```

## Cost

- **OpenAI**: $0-0.30 per video (free $5 trial covers ~20 videos)
- **ElevenLabs**: $0-0.30 per video (10k free chars/month = ~20 videos)
- **Total**: Usually $0 if using free tiers
- **Colab**: 100% FREE

## Features

✅ Works on iPhone, Android, iPad, Mac, Windows, Linux
✅ No installation needed
✅ Free GPU available (optional)
✅ All code runs in browser
✅ Download videos directly
✅ 15GB free storage
✅ Share with team members

## Get API Keys

### OpenAI (Free $5 trial)
1. Go to https://platform.openai.com/signup
2. Sign up with email
3. Verify phone number
4. Get $5 credit automatically
5. Go to https://platform.openai.com/account/api-keys
6. Create new key
7. Copy key (starts with `sk-proj-`)

### ElevenLabs (Free 10k chars/month)
1. Go to https://elevenlabs.io
2. Click "Sign up free"
3. Go to Account → API Key
4. Copy API key
5. Go to Voice Library → Select any voice → Copy Voice ID

## Advanced: Custom Notebook

If you want a full interactive notebook with UI:

1. Go to https://colab.research.google.com
2. Create new notebook
3. Paste the code above
4. Or upload `colab_notebook.ipynb` if you have it

## Tips

**For faster rendering:**
```python
# Add this line before generating:
config.video.preset = "ultrafast"
config.video.output_resolution = [1024, 576]
```

**For higher quality:**
```python
config.video.preset = "slow"
config.video.output_resolution = [1920, 1080]
config.openai.model = "gpt-4o"
```

**Process multiple videos:**
```python
urls = [
    "https://youtube.com/watch?v=URL1",
    "https://youtube.com/watch?v=URL2",
    "https://youtube.com/watch?v=URL3",
]

topics = [
    "Breakcore reaction",
    "Gaming fails",
    "Internet lore",
]

for url, topic in zip(urls, topics):
    build_full_automation_video(url, topic)
```

## Troubleshooting

**\"API key invalid\"**
→ Check your keys at OpenAI.com and ElevenLabs.io

**\"ModuleNotFoundError\"**
→ Rerun the install dependencies cell

**Session disconnected**
→ Click "Reconnect" and continue from where you left off

**Out of memory**
→ Lower the video resolution (1024x576 instead of 1920x1080)

**Slow rendering**
→ Use ultrafast preset and lower resolution

**Download stuck**
→ Refresh page and download again

## Next Steps

1. ✅ Run code in Colab
2. 🎬 Generate 3-5 videos
3. 📱 Download to iPhone
4. 🎥 Upload to YouTube
5. 💰 Start monetizing!

---

**Questions?** Check FAQ.md or open an issue on GitHub!

**Happy creating from your iPhone! 🚀📱**
