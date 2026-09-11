#!/usr/bin/env python3
"""Simple launcher - just run your first video!"""

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Launch automated YouTube reaction channel generator"
    )
    parser.add_argument(
        'url',
        nargs='?',
        default='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        help='YouTube URL to react to (default: Rick Roll)'
    )
    parser.add_argument(
        '--topic',
        type=str,
        default='Reacting to this awesome content',
        help='Reaction topic/context'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output video filename'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Run system checks only'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Process batch from JSON file'
    )
    
    args = parser.parse_args()
    
    # System checks
    if args.check:
        print("Running system checks...")
        import subprocess
        result = subprocess.run([sys.executable, 'quickstart.py'])
        return result.returncode
    
    # Batch processing
    if args.batch:
        print(f"Processing batch: {args.batch}")
        import subprocess
        result = subprocess.run(
            [sys.executable, 'batch_processor.py', '--batch', args.batch]
        )
        return result.returncode
    
    # Single video
    print(f"\nGenerating reaction to: {args.url}")
    print(f"Topic: {args.topic}")
    
    try:
        from main import build_full_automation_video
        
        build_full_automation_video(
            media_url=args.url,
            topic=args.topic,
            output_path=args.output
        )
        print("\n✓ Video generation complete!")
        return 0
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nRun 'python quickstart.py' to check your system setup")
        return 1


if __name__ == "__main__":
    exit(main())
