# Automated YouTube Reaction Channel Generator

A sophisticated automation tool for creating high-energy, AI-driven YouTube reaction videos with audio-reactive PNGTuber avatars.

## Features

✨ **Full Pipeline Automation**
- Download source media via yt-dlp
- Generate AI scripts using GPT-4o with emotional expressions
- Synthesize natural voiceovers via ElevenLabs TTS
- Create audio-reactive avatar clips
- Composite and render final videos

🎭 **Audio-Reactive Avatar System**
- 7 distinct emotional expressions (threatening, smirking, mischievous, hyped, playful, heart_eyes, star_eyes)
- Real-time audio volume analysis
- Dynamic sprite scaling and positioning
- Speech-triggered animation bounces

⚙️ **Professional Configuration**
- YAML-based config with environment variable support
- Pydantic validation for type safety
- Comprehensive logging with file rotation
- Automatic temporary file cleanup

## Installation

### Prerequisites
- Python 3.8+
- FFmpeg (for moviepy)
- API keys for OpenAI and ElevenLabs

### Setup

```bash
# Clone repository
git clone https://github.com/necronwolf1-oss/automated-youtube-reaction-channel.git
cd automated-youtube-reaction-channel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Sprite Assets

Create an `assets/sprites/` directory and add your PNGTuber sprite images:

```
assets/sprites/
├── image_3.png   # threatening (knife pose)
├── image_4.png   # smirking (crossed arms)
├── image_5.png   # mischievous (wolf ears)
├── image_6.png   # hyped (open mouth)
├── image_7.png   # playful (wink)
├── image_8.png   # heart_eyes (love)
└── image_9.png   # star_eyes (amazed)
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# API Settings
api:
  openai_key: "${OPENAI_API_KEY}"
  elevenlabs_key: "${ELEVENLABS_API_KEY}"
  elevenlabs_voice_id: "${ELEVENLABS_VOICE_ID}"

# Video Output
video:
  output_resolution: [1280, 720]
  fps: 24
  codec: "libx264"
  preset: "medium"  # faster encode vs slower=better quality

# Avatar Behavior
avatar:
  height: 380
  position: ["right", "bottom"]
  audio_reactivity:
    enabled: true
    min_volume_threshold: 0.15
    max_scale_factor: 1.08

# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/automation.log"
```

## Usage

### Basic Usage

```python
from main import build_full_automation_video

build_full_automation_video(
    media_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    topic="Reacting to underground breakcore tracks"
)
```

### Custom Output Path

```python
build_full_automation_video(
    media_url="https://www.youtube.com/watch?v=...",
    topic="My reaction topic",
    output_path="my_video.mp4"
)
```

### Command Line

```bash
python main.py
```

## Architecture

### Pipeline Stages

```
┌─────────────────────┐
│  Download Media     │ (yt-dlp)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Generate Script     │ (OpenAI GPT-4o)
│ + Emotions          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Per-Scene Processing               │
├─────────────┬───────────────────────┤
│ Voiceover   │  Sprite Selection     │
│ (ElevenLabs)│  + Audio Reactivity   │
└─────────────┴───────────┬───────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │ Composite Layers     │
              │ (Background + Avatar)│
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Concatenate Scenes   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Render Final Video   │
              │ (H.264 MP4)          │
              └──────────────────────┘
```

### Module Structure

- **`main.py`** - Core pipeline orchestration
- **`config.py`** - Configuration management with Pydantic validation
- **`logger_setup.py`** - Centralized logging with colors and file rotation
- **`config.yaml`** - User-facing configuration
- **`.env`** - Sensitive API keys (git-ignored)

## Logging

Logs are written to both console (with colors) and `logs/automation.log`:

```
2024-01-15 14:23:45 - INFO - [*] Downloading source media: https://...
2024-01-15 14:23:48 - DEBUG - ✓ Source media downloaded: .temp/source_clip.mp4
2024-01-15 14:23:50 - INFO - [*] Generating script for topic: Breakcore
2024-01-15 14:24:02 - INFO - ✓ Generated script with 5 scenes
```

## Error Handling

Comprehensive error handling with detailed logging:

- **API Failures**: Automatic error messages with status codes
- **File Issues**: Missing sprites or audio files detected early
- **Validation**: Timestamp conflicts caught before rendering
- **Cleanup**: Automatic temporary file removal on exit or error

## Performance Tips

1. **Faster Encoding**: Set `video.preset: "fast"` in config.yaml
2. **Smaller Videos**: Reduce `video.output_resolution`
3. **GPU Acceleration**: Install FFmpeg with NVIDIA NVENC support
4. **Parallel Processing**: Use `multiprocessing` for large batches

## Troubleshooting

### "Sprite file not found"
- Ensure sprite PNGs are in `assets/sprites/` with correct filenames
- Check config.yaml sprite paths match actual files

### "API key error"
- Verify `.env` file exists and has correct keys
- Check keys are valid on OpenAI/ElevenLabs dashboards
- Restart Python to reload environment variables

### "Download failed"
- Check media URL is valid
- Ensure yt-dlp is updated: `pip install --upgrade yt-dlp`
- Try different media URL format

### "No audio in output"
- Verify ElevenLabs key and voice ID are correct
- Check API response with `logging.level: "DEBUG"`
- Ensure audio file was generated (check `.temp/` directory)

## Dependencies

See `requirements.txt` for pinned versions. Key packages:

- **moviepy** - Video composition and rendering
- **yt-dlp** - Media downloading
- **openai** - GPT-4o script generation
- **elevenlabs** - TTS voice synthesis
- **pydantic** - Configuration validation
- **requests** - HTTP API calls
- **numpy** - Audio processing

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review logs in `logs/automation.log`

## Roadmap

- [ ] Batch video processing
- [ ] Custom emotion expressions
- [ ] Real-time preview mode
- [ ] Web UI dashboard
- [ ] Cloud rendering support
- [ ] Multi-language support

---

**Built with ❤️ for creators who like weird internet lore and breakcore**
