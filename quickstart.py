#!/usr/bin/env python3
"""Quick start script for first-time users."""

import sys
import os
from pathlib import Path


def check_system():
    """Verify all system requirements are met."""
    print("\n" + "="*60)
    print("SYSTEM REQUIREMENTS CHECK")
    print("="*60)
    
    checks_passed = 0
    checks_total = 0
    
    # Check Python version
    checks_total += 1
    py_version = sys.version_info
    if py_version.major == 3 and py_version.minor >= 8:
        print(f"✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        checks_passed += 1
    else:
        print(f"✗ Python {py_version.major}.{py_version.minor} (need 3.8+)")
    
    # Check FFmpeg
    checks_total += 1
    result = os.system('ffmpeg -version > /dev/null 2>&1')
    if result == 0:
        print("✓ FFmpeg installed")
        checks_passed += 1
    else:
        print("✗ FFmpeg not found (install with: brew/apt/choco install ffmpeg)")
    
    # Check .env file
    checks_total += 1
    if Path('.env').exists():
        print("✓ .env file exists")
        checks_passed += 1
    else:
        print("✗ .env file missing (run: cp .env.example .env)")
    
    # Check sprites
    checks_total += 1
    sprite_dir = Path('assets/sprites')
    if sprite_dir.exists():
        pngs = list(sprite_dir.glob('*.png'))
        if len(pngs) >= 7:
            print(f"✓ Sprites found ({len(pngs)} PNG files)")
            checks_passed += 1
        else:
            print(f"✗ Only {len(pngs)}/7 sprites found")
    else:
        print("✗ assets/sprites directory not found")
    
    # Check config
    checks_total += 1
    if Path('config.yaml').exists():
        print("✓ config.yaml exists")
        checks_passed += 1
    else:
        print("✗ config.yaml missing")
    
    # Check dependencies
    checks_total += 1
    try:
        import moviepy
        import yt_dlp
        import openai
        import requests
        from config import get_config
        from logger_setup import get_logger
        print("✓ All Python dependencies installed")
        checks_passed += 1
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
    
    print("\n" + "-"*60)
    print(f"Status: {checks_passed}/{checks_total} checks passed")
    print("-"*60)
    
    return checks_passed == checks_total


def test_api_keys():
    """Test that API keys are configured correctly."""
    print("\n" + "="*60)
    print("API KEY VERIFICATION")
    print("="*60)
    
    try:
        from config import get_config
        from logger_setup import get_logger
        import requests
        
        logger = get_logger()
        config = get_config()
        
        # Test OpenAI
        print("\nTesting OpenAI...")
        try:
            import openai
            openai.api_key = config.api.openai_key
            # Just list models to verify key works
            result = openai.Model.list()
            print(f"✓ OpenAI API key valid")
            print(f"  Model: {config.openai.model}")
        except Exception as e:
            print(f"✗ OpenAI error: {str(e)[:100]}")
            return False
        
        # Test ElevenLabs
        print("\nTesting ElevenLabs...")
        headers = {'xi-api-key': config.api.elevenlabs_key}
        response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            char_count = data.get('character_count', 0)
            print(f"✓ ElevenLabs API key valid")
            print(f"  Characters used: {char_count} / 10,000")
        else:
            print(f"✗ ElevenLabs error: {response.status_code} - {response.text[:100]}")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Configuration error: {str(e)}")
        return False


def test_sprite_files():
    """Verify all sprite files are valid."""
    print("\n" + "="*60)
    print("SPRITE VALIDATION")
    print("="*60)
    
    try:
        from config import get_config
        from PIL import Image
        
        config = get_config()
        all_valid = True
        
        for emotion, sprite_path in config.sprites.items():
            try:
                img = Image.open(sprite_path)
                size = img.size
                print(f"✓ {emotion:15} {sprite_path:30} {size}")
            except Exception as e:
                print(f"✗ {emotion:15} {sprite_path:30} {str(e)[:40]}")
                all_valid = False
        
        return all_valid
    
    except Exception as e:
        print(f"✗ Sprite validation error: {str(e)}")
        return False


def run_quick_test():
    """Run a quick script generation test without full video processing."""
    print("\n" + "="*60)
    print("QUICK TEST: Script Generation")
    print("="*60)
    
    try:
        from config import get_config
        from logger_setup import get_logger
        from main import generate_channel_script
        
        logger = get_logger()
        config = get_config()
        
        print("\nGenerating test script (this uses ~$0.01 of your OpenAI credits)...")
        
        script = generate_channel_script(
            topic="Test reaction to internet content",
            video_title="Test Video",
            config=config
        )
        
        scenes = script.get('scenes', [])
        print(f"✓ Script generated successfully!")
        print(f"  Scenes: {len(scenes)}")
        
        for idx, scene in enumerate(scenes[:2], 1):
            print(f"\n  Scene {idx}:")
            print(f"    Emotion: {scene.get('emotion')}")
            print(f"    Duration: {scene.get('end_time', 0) - scene.get('start_time', 0):.1f}s")
            narration = scene.get('narration', '')[:60]
            print(f"    Text: {narration}...")
        
        return True
    
    except Exception as e:
        print(f"✗ Script generation failed: {str(e)}")
        print("  Check your API keys and internet connection")
        return False


def show_next_steps():
    """Display next steps for user."""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    print("""
1. Run your first video:
   python3 main.py
   
2. Or process multiple videos:
   python3 batch_processor.py --batch examples/batch_example.json
   
3. Customize configuration:
   nano config.yaml
   
4. View logs in real-time:
   tail -f logs/automation.log
   
5. Check FAQ for common issues:
   See FAQ.md
   
6. Try different script styles:
   python3 examples/prompt_templates.py comedy
   python3 examples/prompt_templates.py horror
   python3 examples/prompt_templates.py educational
    """)


def main():
    """Run all startup checks."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Automated YouTube Reaction Channel - Quick Start".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run checks
    system_ok = check_system()
    api_ok = test_api_keys() if system_ok else False
    sprites_ok = test_sprite_files() if system_ok else False
    
    if system_ok and api_ok and sprites_ok:
        print("\n" + "="*60)
        print("✓ ALL CHECKS PASSED - SYSTEM READY!")
        print("="*60)
        
        # Optional quick test
        response = input("\nRun quick API test? (y/n): ").strip().lower()
        if response == 'y':
            test_ok = run_quick_test()
        
        show_next_steps()
        return 0
    else:
        print("\n" + "="*60)
        print("✗ SOME CHECKS FAILED - FIX ISSUES ABOVE")
        print("="*60)
        print("\nCommon fixes:")
        print("  - Install FFmpeg: https://ffmpeg.org/download.html")
        print("  - Copy .env file: cp .env.example .env")
        print("  - Add API keys to .env file")
        print("  - Add sprites to assets/sprites/")
        print("  - Install Python deps: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    exit(main())
