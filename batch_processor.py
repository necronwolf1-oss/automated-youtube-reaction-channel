"""Batch processing utility for generating multiple videos."""
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from config import get_config
from logger_setup import get_logger
from main import build_full_automation_video

logger = get_logger()


def load_batch_file(filepath: str) -> List[Dict]:
    """Load batch configuration from JSON file.
    
    Args:
        filepath: Path to JSON file with batch config
        
    Returns:
        List of video configurations
    """
    logger.info(f"Loading batch file: {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        videos = data
    elif isinstance(data, dict) and 'videos' in data:
        videos = data['videos']
    else:
        raise ValueError("Batch file must contain list or dict with 'videos' key")
    
    logger.info(f"Loaded {len(videos)} videos from batch file")
    return videos


def process_batch(videos: List[Dict], dry_run: bool = False, skip_failed: bool = True):
    """Process multiple videos in batch.
    
    Args:
        videos: List of video configurations
        dry_run: If True, only validate without processing
        skip_failed: If True, continue on error; if False, stop
    """
    config = get_config()
    results = {
        'timestamp': datetime.now().isoformat(),
        'total': len(videos),
        'successful': 0,
        'failed': 0,
        'videos': []
    }
    
    logger.info("=" * 60)
    logger.info(f"Starting batch processing: {len(videos)} videos")
    logger.info(f"Dry run: {dry_run}")
    logger.info("=" * 60)
    
    for idx, video_config in enumerate(videos, 1):
        video_info = {
            'index': idx,
            'url': video_config.get('media_url'),
            'topic': video_config.get('topic'),
            'output': video_config.get('output_path'),
            'status': 'pending',
            'error': None
        }
        
        logger.info(f"\n[{idx}/{len(videos)}] Processing: {video_info['topic']}")
        
        try:
            # Validate config
            if not video_config.get('media_url'):
                raise ValueError("media_url is required")
            if not video_config.get('topic'):
                raise ValueError("topic is required")
            
            if dry_run:
                logger.info(f"[DRY RUN] Would process: {video_info['topic']}")
                video_info['status'] = 'validated'
            else:
                # Process video
                output_path = video_config.get('output_path')
                build_full_automation_video(
                    media_url=video_config['media_url'],
                    topic=video_config['topic'],
                    output_path=output_path
                )
                video_info['status'] = 'completed'
                results['successful'] += 1
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}", exc_info=True)
            video_info['status'] = 'failed'
            video_info['error'] = str(e)
            results['failed'] += 1
            
            if not skip_failed:
                logger.critical("Stopping batch due to error (skip_failed=False)")
                break
        
        results['videos'].append(video_info)
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Batch Processing Summary")
    logger.info("=" * 60)
    logger.info(f"Total: {results['total']}")
    logger.info(f"Successful: {results['successful']}")
    logger.info(f"Failed: {results['failed']}")
    logger.info(f"Success Rate: {(results['successful']/results['total']*100):.1f}%")
    
    # Save results
    results_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to: {results_file}")
    
    return results


def create_batch_template(output_file: str = "batch_template.json"):
    """Create a template batch configuration file.
    
    Args:
        output_file: Output filename
    """
    template = {
        "videos": [
            {
                "media_url": "https://www.youtube.com/watch?v=VIDEO_ID_1",
                "topic": "Reacting to underground breakcore tracks",
                "output_path": "output_video_1.mp4"
            },
            {
                "media_url": "https://www.youtube.com/watch?v=VIDEO_ID_2",
                "topic": "Reacting to weird internet lore",
                "output_path": "output_video_2.mp4"
            },
            {
                "media_url": "https://www.youtube.com/watch?v=VIDEO_ID_3",
                "topic": "Gaming fails compilation reaction",
                "output_path": "output_video_3.mp4"
            }
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    logger.info(f"Template created: {output_file}")
    print(f"Template saved to {output_file}")
    print("Edit this file with your video URLs and topics, then run:")
    print(f"  python batch_processor.py --batch {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch process multiple YouTube reaction videos"
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Path to batch JSON file'
    )
    parser.add_argument(
        '--template',
        action='store_true',
        help='Create a template batch file'
    )
    parser.add_argument(
        '--template-file',
        type=str,
        default='batch_template.json',
        help='Output filename for template'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate without processing'
    )
    parser.add_argument(
        '--continue-on-error',
        action='store_true',
        default=True,
        help='Continue processing on error'
    )
    
    args = parser.parse_args()
    
    if args.template:
        create_batch_template(args.template_file)
    elif args.batch:
        videos = load_batch_file(args.batch)
        process_batch(videos, dry_run=args.dry_run, skip_failed=args.continue_on_error)
    else:
        parser.print_help()
