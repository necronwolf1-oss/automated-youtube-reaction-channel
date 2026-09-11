"""Automated YouTube Reaction Channel Generator - Main Entry Point.

This module orchestrates the full pipeline:
1. Download source media via yt-dlp
2. Generate AI-driven scripts with emotions
3. Synthesize voiceovers via ElevenLabs TTS
4. Create audio-reactive avatar clips
5. Composite and render final video
"""

import os
import sys
import json
import tempfile
import atexit
from pathlib import Path
from typing import Dict, List, Optional
import requests
import numpy as np
import yt_dlp
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
)

from config import get_config, AppConfig
from logger_setup import get_logger

logger = get_logger()

# Global temp files list for cleanup
TEMP_FILES: List[str] = []


def cleanup_temp_files():
    """Clean up temporary files on exit."""
    config = get_config()
    if not config.files.cleanup_on_exit:
        return
    
    logger.info("Cleaning up temporary files...")
    for temp_file in TEMP_FILES:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                logger.debug(f"Deleted: {temp_file}")
        except Exception as e:
            logger.warning(f"Failed to delete temp file {temp_file}: {e}")
    
    # Clean up temp directory
    try:
        temp_dir = Path(config.files.temp_directory)
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()
            logger.info(f"Removed empty temp directory: {temp_dir}")
    except Exception as e:
        logger.warning(f"Failed to remove temp directory: {e}")


# Register cleanup on exit
atexit.register(cleanup_temp_files)


def validate_sprite_files(config: AppConfig) -> bool:
    """Validate that all required sprite files exist.
    
    Args:
        config: Application configuration
        
    Returns:
        True if all sprites valid
        
    Raises:
        FileNotFoundError: If any sprite is missing
    """
    logger.info("Validating sprite files...")
    for emotion, sprite_path in config.sprites.items():
        if not Path(sprite_path).exists():
            logger.error(f"Missing sprite for '{emotion}': {sprite_path}")
            raise FileNotFoundError(f"Sprite file not found: {sprite_path}")
        logger.debug(f"✓ {emotion}: {sprite_path}")
    
    logger.info(f"✓ All {len(config.sprites)} sprites validated")
    return True


def download_reaction_source(media_url: str, config: AppConfig) -> str:
    """Download youtube/niche video clips via yt-dlp to react to.
    
    Args:
        media_url: URL of the media to download
        config: Application configuration
        
    Returns:
        Path to downloaded video file
        
    Raises:
        RuntimeError: If download fails
    """
    logger.info(f"[*] Downloading source media: {media_url}")
    
    temp_dir = Path(config.files.temp_directory)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = temp_dir / "source_clip.mp4"
    TEMP_FILES.append(str(output_file))
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(output_file),
        'overwrites': True,
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"Using yt-dlp with options: {ydl_opts}")
            ydl.download([media_url])
        
        if not output_file.exists():
            raise RuntimeError("Download succeeded but file not found")
        
        logger.info(f"✓ Source media downloaded: {output_file}")
        return str(output_file)
    
    except Exception as e:
        logger.error(f"Download failed: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to download media: {str(e)}") from e


def generate_channel_script(topic: str, video_title: str, config: AppConfig) -> Dict:
    """Call OpenAI API to create persona script tagged with reactions and timestamps.
    
    Args:
        topic: Topic/context for the reaction
        video_title: Title of the video being reacted to
        config: Application configuration
        
    Returns:
        Dictionary with scenes containing narration, emotion, and timing
        
    Raises:
        requests.HTTPError: If API call fails
        json.JSONDecodeError: If response is invalid JSON
    """
    logger.info(f"[*] Generating script for topic: {topic}")
    
    system_prompt = f"""You are the writer for a high-energy, comedy-horror YouTube reaction channel focused on niche music, breakcore, and weird internet lore.
    
Your output MUST be a strict JSON object with this format:
{{
    "scenes": [
        {{
            "narration": "Script text here...",
            "emotion": "threatening | smirking | mischievous | hyped | playful | heart_eyes | star_eyes",
            "start_time": 0.0,
            "end_time": 5.0
        }}
    ]
}}

Each scene should be 3-8 sentences. Use the available emotions expressively.
"""
    
    headers = {
        "Authorization": f"Bearer {config.api.openai_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": config.openai.model,
        "response_format": {"type": config.openai.response_format},
        "temperature": config.openai.temperature,
        "max_tokens": config.openai.max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Create a script reacting to: {video_title}\nContext: {topic}",
            },
        ],
    }
    
    try:
        logger.debug("Calling OpenAI API...")
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        res.raise_for_status()
        
        response_data = res.json()
        script_content = response_data["choices"][0]["message"]["content"]
        script_data = json.loads(script_content)
        
        logger.info(f"✓ Generated script with {len(script_data.get('scenes', []))} scenes")
        logger.debug(f"Script: {json.dumps(script_data, indent=2)}")
        
        return script_data
    
    except requests.HTTPError as e:
        logger.error(f"OpenAI API error: {e.response.status_code} - {e.response.text}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in API response: {e}")
        raise
    except Exception as e:
        logger.error(f"Script generation failed: {str(e)}", exc_info=True)
        raise


def generate_voiceover(text: str, filename: str, config: AppConfig) -> str:
    """Generate audio file via ElevenLabs TTS.
    
    Args:
        text: Text to synthesize
        filename: Output audio filename
        config: Application configuration
        
    Returns:
        Path to generated audio file
        
    Raises:
        requests.HTTPError: If API call fails
        IOError: If file write fails
    """
    logger.info(f"[*] Generating voiceover for text ({len(text)} chars)...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.api.elevenlabs_voice_id}"
    headers = {
        "xi-api-key": config.api.elevenlabs_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": config.voice.model_id,
        "voice_settings": {
            "stability": config.voice.stability,
            "similarity_boost": config.voice.similarity_boost,
        },
    }
    
    try:
        logger.debug(f"Calling ElevenLabs API for voice: {config.api.elevenlabs_voice_id}")
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(res.content)
        
        logger.info(f"✓ Voiceover generated: {filename}")
        TEMP_FILES.append(filename)  # Mark for cleanup
        return filename
    
    except requests.HTTPError as e:
        logger.error(f"ElevenLabs API error: {e.response.status_code} - {e.response.text}")
        raise
    except IOError as e:
        logger.error(f"Failed to write audio file {filename}: {e}")
        raise
    except Exception as e:
        logger.error(f"Voiceover generation failed: {str(e)}", exc_info=True)
        raise


def create_reactive_avatar_clip(
    audio_path: str, emotion: str, config: AppConfig
) -> CompositeVideoClip:
    """Create a PNGTuber avatar clip that pulses and scales dynamically to speech audio.
    
    Args:
        audio_path: Path to audio file
        emotion: Emotion expression to use
        config: Application configuration
        
    Returns:
        CompositeVideoClip with reactive avatar
        
    Raises:
        FileNotFoundError: If sprite or audio file not found
        Exception: If video processing fails
    """
    logger.info(f"[*] Creating reactive avatar clip ({emotion})...")
    
    if emotion not in config.sprites:
        logger.error(f"Unknown emotion: {emotion}")
        raise ValueError(f"Unknown emotion: {emotion}")
    
    sprite_path = config.sprites[emotion]
    if not Path(sprite_path).exists():
        logger.error(f"Sprite file not found: {sprite_path}")
        raise FileNotFoundError(f"Sprite file not found: {sprite_path}")
    
    if not Path(audio_path).exists():
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    try:
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Extract audio volume array to trigger speech-bounce effect
        logger.debug("Extracting audio volume envelope...")
        sound_array = audio.to_soundarray(fps=config.video.fps)
        
        if sound_array.size == 0:
            logger.warning("Empty sound array, using default envelope")
            volume_envelope = np.ones(int(duration * config.video.fps))
        else:
            if len(sound_array.shape) > 1:
                volume_envelope = np.sqrt(np.mean(sound_array**2, axis=1))
            else:
                volume_envelope = np.abs(sound_array)
            
            max_vol = np.max(volume_envelope)
            if max_vol > 0:
                volume_envelope = volume_envelope / max_vol
            else:
                volume_envelope = np.ones_like(volume_envelope)
        
        reactivity = config.avatar.audio_reactivity
        threshold = reactivity["min_volume_threshold"]
        max_scale = reactivity["max_scale_factor"]
        
        def make_frame(get_frame, t):
            """Apply dynamic scaling based on volume."""
            frame_idx = min(int(t * config.video.fps), len(volume_envelope) - 1)
            vol = volume_envelope[frame_idx]
            
            if vol > threshold:
                scale_factor = 1.0 + (vol * (max_scale - 1.0))
            else:
                scale_factor = 1.0
            
            frame = get_frame(t)
            # Scale frame while maintaining aspect ratio
            height, width = frame.shape[:2]
            new_height = int(height * scale_factor)
            new_width = int(width * scale_factor)
            
            if new_height != height or new_width != width:
                import cv2
                frame = cv2.resize(frame, (new_width, new_height))
            
            return frame
        
        # Load sprite and build clip
        logger.debug(f"Loading sprite: {sprite_path}")
        sprite_clip = ImageClip(sprite_path).set_duration(duration)
        
        # Apply audio-reactive transformation
        if reactivity["enabled"]:
            logger.debug("Applying audio reactivity filter...")
            reactive_clip = sprite_clip.fl(make_frame)
        else:
            reactive_clip = sprite_clip
        
        # Resize and position
        reactive_clip = reactive_clip.resize(height=config.avatar.height)
        reactive_clip = reactive_clip.set_position(
            (config.avatar.position[0], config.avatar.position[1])
        )
        
        # Add audio
        reactive_clip = reactive_clip.set_audio(audio)
        
        logger.info(f"✓ Avatar clip created ({emotion}, {duration:.2f}s)")
        return reactive_clip
    
    except Exception as e:
        logger.error(f"Avatar clip creation failed: {str(e)}", exc_info=True)
        raise


def validate_script_timestamps(script_data: Dict, bg_duration: float, config: AppConfig) -> bool:
    """Validate that script timestamps fit within background video duration.
    
    Args:
        script_data: Script data from OpenAI
        bg_duration: Duration of background video
        config: Application configuration
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If timestamps are invalid or exceed duration
    """
    if not config.script.enable_timestamp_validation:
        logger.debug("Timestamp validation disabled")
        return True
    
    logger.info("Validating script timestamps...")
    
    for idx, scene in enumerate(script_data.get("scenes", [])):
        start_time = scene.get("start_time", 0.0)
        end_time = scene.get("end_time", start_time + config.script.default_scene_duration)
        duration = end_time - start_time
        
        if duration < config.script.min_scene_duration:
            logger.warning(
                f"Scene {idx} duration ({duration:.2f}s) below minimum "
                f"({config.script.min_scene_duration}s), adjusting..."
            )
            scene["end_time"] = start_time + config.script.min_scene_duration
        
        if duration > config.script.max_scene_duration:
            logger.warning(
                f"Scene {idx} duration ({duration:.2f}s) exceeds maximum "
                f"({config.script.max_scene_duration}s), truncating..."
            )
            scene["end_time"] = start_time + config.script.max_scene_duration
        
        if start_time >= bg_duration:
            logger.error(
                f"Scene {idx} start_time ({start_time}s) >= background duration ({bg_duration}s)"
            )
            raise ValueError(f"Scene {idx} exceeds background video duration")
        
        logger.debug(
            f"Scene {idx}: {start_time:.2f}s - {scene.get('end_time', 0):.2f}s ✓"
        )
    
    logger.info("✓ All timestamps validated")
    return True


def build_full_automation_video(media_url: str, topic: str, output_path: Optional[str] = None):
    """Orchestrate the full video generation pipeline.
    
    Args:
        media_url: URL of media to react to
        topic: Topic/context for reactions
        output_path: Optional custom output path
        
    Raises:
        Exception: If any pipeline step fails
    """
    config = get_config()
    
    logger.info("=" * 60)
    logger.info("Starting Automated YouTube Reaction Channel Generation")
    logger.info("=" * 60)
    
    try:
        # Validate sprites
        validate_sprite_files(config)
        
        # 1. Download Source Media
        logger.info("\n[STEP 1/5] Downloading Source Media")
        source_video_path = download_reaction_source(media_url, config)
        bg_video = VideoFileClip(source_video_path).resize(
            width=config.video.output_resolution[0],
            height=config.video.output_resolution[1],
        )
        logger.info(f"Background video loaded: {bg_video.duration:.2f}s")
        
        # 2. Generate Script
        logger.info("\n[STEP 2/5] Generating AI Script")
        script_data = generate_channel_script(topic, "Niche Breakcore Horror Reaction", config)
        validate_script_timestamps(script_data, bg_video.duration, config)
        
        # 3. Process Scenes
        logger.info(f"\n[STEP 3/5] Processing {len(script_data.get('scenes', []))} Scenes")
        rendered_scenes = []
        
        for idx, scene in enumerate(script_data.get("scenes", [])):
            logger.info(f"\nProcessing scene {idx + 1}...")
            
            # Generate voiceover
            temp_dir = Path(config.files.temp_directory)
            temp_dir.mkdir(parents=True, exist_ok=True)
            audio_file = str(temp_dir / f"audio_{idx}.mp3")
            
            narration = scene.get("narration", "")
            emotion = scene.get("emotion", "smirking")
            start_time = scene.get("start_time", 0.0)
            
            generate_voiceover(narration, audio_file, config)
            audio_duration = AudioFileClip(audio_file).duration
            end_time = start_time + audio_duration
            
            # Clip background video
            logger.debug(f"Clipping background from {start_time:.2f}s to {end_time:.2f}s")
            safe_end = min(end_time, bg_video.duration)
            sub_bg = bg_video.subclip(start_time, safe_end)
            
            # Build avatar overlay
            avatar_clip = create_reactive_avatar_clip(audio_file, emotion, config)
            
            # Composite
            final_scene = CompositeVideoClip([sub_bg, avatar_clip])
            rendered_scenes.append(final_scene)
            logger.info(f"✓ Scene {idx + 1} complete")
        
        # 4. Concatenate
        logger.info("\n[STEP 4/5] Concatenating Scenes")
        final_video = concatenate_videoclips(rendered_scenes, method="compose")
        logger.info(f"✓ Final video duration: {final_video.duration:.2f}s")
        
        # 5. Export
        logger.info("\n[STEP 5/5] Rendering Video")
        output_file = output_path or config.video.output_filename
        logger.info(f"Writing to {output_file} at {config.video.fps}fps...")
        
        final_video.write_videofile(
            output_file,
            fps=config.video.fps,
            codec=config.video.codec,
            preset=config.video.preset,
            audio_codec="aac",
            verbose=False,
            logger=logger,
        )
        
        logger.info("=" * 60)
        logger.info(f"✓ Video Render Complete: {output_file}")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"\n❌ Pipeline failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Test execution on a target YouTube URL / Niche Media Clip
    TARGET_MEDIA = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    build_full_automation_video(
        TARGET_MEDIA, "Reacting to underground dark-step breakcore tracks"
    )
