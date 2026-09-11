"""
AUTOMATED YOUTUBE REACTION CHANNEL - GOOGLE COLAB VERSION
Run this directly in Google Colab on your iPhone!

Instructions:
1. Go to https://colab.research.google.com
2. Create new notebook
3. Copy this entire file into a cell
4. Run the cell
5. Follow the prompts
"""

print("Installing dependencies...")
import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "-q", "moviepy", "yt-dlp", "openai", "elevenlabs", "pydantic", "python-dotenv", "colorama", "pillow"], check=False)
subprocess.run(["apt-get", "install", "-y", "ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✓ Dependencies installed\n")

import os
from getpass import getpass
from pathlib import Path

print("="*60)
print("AUTOMATED YOUTUBE REACTION CHANNEL - COLAB")
print("="*60)

print("\n[STEP 1] Enter your API keys")
print("(Keys won't display as you type - that's normal)\n")

openai_key = getpass("OpenAI API Key (starts with sk-): ")
elevenlabs_key = getpass("ElevenLabs API Key: ")
voice_id = input("ElevenLabs Voice ID (e.g., 21m00Tcm4TlvDq8ikWAM): ")

os.environ['OPENAI_API_KEY'] = openai_key
os.environ['ELEVENLABS_API_KEY'] = elevenlabs_key
os.environ['ELEVENLABS_VOICE_ID'] = voice_id

print("\n✓ API keys configured\n")

print("[STEP 2] Downloading project files...")
subprocess.run(["git", "clone", "https://github.com/necronwolf1-oss/automated-youtube-reaction-channel.git"], 
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.chdir('automated-youtube-reaction-channel')
print("✓ Project downloaded\n")

print("[STEP 3] Setting up configuration...")
env_content = f"""OPENAI_API_KEY={openai_key}
ELEVENLABS_API_KEY={elevenlabs_key}
ELEVENLABS_VOICE_ID={voice_id}
"""

with open('.env', 'w') as f:
    f.write(env_content)

print("✓ Configuration created\n")

print("[STEP 4] Creating sprite placeholders...")
from PIL import Image, ImageDraw

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

print("[STEP 5] Testing configuration...")
try:
    from config import get_config
    config = get_config()
    print(f"✓ Configuration valid")
    print(f"  - OpenAI Model: {config.openai.model}")
    print(f"  - Video Resolution: {config.video.output_resolution}")
    print(f"  - Avatar Height: {config.avatar.height}\n")
except Exception as e:
    print(f"✗ Configuration error: {str(e)}\n")
    print("Check your API keys and try again")
    exit(1)

print("="*60)
print("[STEP 6] READY TO GENERATE VIDEO!")
print("="*60)

print("\nEnter your video details:\n")
youtube_url = input("YouTube URL: ")
reaction_topic = input("Reaction topic (e.g., 'Reacting to breakcore music'): ")

if not youtube_url or not reaction_topic:
    print("✗ URL and topic are required")
    exit(1)

print("\n" + "="*60)
print("GENERATING VIDEO")
print("="*60)
print(f"\nURL: {youtube_url}")
print(f"Topic: {reaction_topic}")
print("\nThis will take 10-20 minutes. Grab a coffee! ☕\n")

try:
    from main import build_full_automation_video
    build_full_automation_video(
        media_url=youtube_url,
        topic=reaction_topic
    )
    print("\n" + "="*60)
    print("✓ VIDEO GENERATED SUCCESSFULLY!")
    print("="*60 + "\n")
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check your YouTube URL is valid")
    print("2. Verify your API keys at OpenAI.com and ElevenLabs.io")
    print("3. Check internet connection")
    exit(1)

print("[STEP 7] Downloading video...\n")

from google.colab import files

mp4_files = list(Path('.').glob('*.mp4'))

if mp4_files:
    print(f"✓ Found {len(mp4_files)} video(s):\n")
    for video_file in mp4_files:
        size_mb = video_file.stat().st_size / (1024*1024)
        print(f"  - {video_file.name} ({size_mb:.1f} MB)")
    
    print("\nStarting download...\n")
    for video_file in mp4_files:
        files.download(str(video_file))
        print(f"✓ Downloaded: {video_file.name}")
else:
    print("✗ No videos found")
    exit(1)

print("\n" + "="*60)
print("✓ ALL DONE!")
print("="*60)
print("\nYour video is downloading to your device.")
print("Upload to YouTube and start monetizing! 🚀")
