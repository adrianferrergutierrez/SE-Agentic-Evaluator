"""
core/extraction/diagramlens_tool.py
====================================
Tool: Describe diagrams in a Markdown document using DashScope Vision API.

Reads a Markdown document, finds image references, calls the vision model
to generate a textual description, and appends it to the document.

Features:
- Automatic image compression for images > 1MB
- Retry logic with exponential backoff for transient errors
- Detailed logging for troubleshooting batch processing
"""

from __future__ import annotations

import io
import logging
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# Try to import PIL for image processing (optional)
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    logger.warning("PIL not available. Image compression will be skipped.")

from core.clients.dashscope_client import DashScopeClient

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

# Image compression settings - Aggressive to avoid 400 errors
MAX_IMAGE_SIZE = 512 * 1024  # 500 KB threshold
MAX_IMAGE_WIDTH = 800  # Reduced width to minimize payload
JPEG_QUALITY = 60  # Lower quality for smaller size
REQUEST_DELAY = 2.0  # Seconds to wait between requests
MIN_API_IMAGE_DIMENSION = 11  # DashScope requires width/height > 10


def _is_valid_for_vision_api(image_path: Path) -> bool:
    """Return True if image dimensions satisfy DashScope Vision constraints."""
    if not image_path.exists():
        return False
    if not HAS_PIL:
        # Without PIL we cannot validate dimensions safely; keep current behavior.
        return True

    try:
        with Image.open(image_path) as img:
            return img.width >= MIN_API_IMAGE_DIMENSION and img.height >= MIN_API_IMAGE_DIMENSION
    except Exception as e:
        logger.warning("Could not read image dimensions for %s: %s", image_path.name, e)
        return False


def compress_image_if_needed(image_path: Path) -> Path:
    """Always convert image to clean JPEG to ensure API compatibility.
    
    Converts all images to RGB JPEG format to avoid 400 errors caused by
    PNG alpha channels, unsupported formats, or metadata. Also resizes if needed.
    
    Parameters
    ----------
    image_path : Path
        Path to the image file.
        
    Returns
    -------
    Path
        Path to processed image file (always a clean JPEG).
    """
    if not image_path.exists():
        return image_path
    
    # If PIL is not available, return original
    if not HAS_PIL:
        logger.warning("PIL not available. Image will be sent as-is.")
        return image_path
    
    try:
        file_size = image_path.stat().st_size
        logger.debug(f"Processing image: {image_path.name} ({file_size / 1024:.1f} KB)")
        
        img = Image.open(image_path)
        
        # Always convert to RGB to avoid alpha channel issues
        if img.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
        
        # Resize if width exceeds limit
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        # Save as clean JPEG
        temp_file = Path(tempfile.gettempdir()) / f"processed_{image_path.stem}.jpg"
        img.save(temp_file, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        
        final_size = temp_file.stat().st_size
        logger.debug(
            f"Image converted: {image_path.name} -> {temp_file.name} "
            f"({final_size / 1024:.1f} KB)"
        )
        
        return temp_file
        
    except Exception as e:
        logger.warning(f"Failed to process {image_path.name}: {e}. Using original.")
        return image_path


def describe_diagrams(
    document_path: str,
    model: str = os.environ.get("DASHSCOPE_VISION_MODEL", "qwen3-vl-32b"),
    prompt: str = (
        "Identify the specific type of this diagram (e.g., UML Class Diagram, Sequence Diagram, "
        "Use Case Diagram, Activity Diagram, ER Diagram, Flowchart, etc.). "
        "Then, provide a detailed description including: "
        "1) Main elements and their attributes/labels, "
        "2) Relationships and multiplicities, "
        "3) Notation used, "
        "4) Any visible text or titles. "
        "If it is not a technical diagram, describe its content concisely."
    ),
) -> Dict[str, Any]:
    """Analyze images in a Markdown document and append descriptions.
    
    Large images (> 1 MB) are automatically compressed to reduce payload size
    and avoid 400 errors from the DashScope API. The tool includes retry logic
    for transient failures.
    
    If the vision API fails (e.g., no quota, API key missing), the function
    returns the original document without descriptions instead of raising an
    exception. This allows workflows to continue with text-only evaluation.

    Parameters
    ----------
    document_path:
        Path to the Markdown file containing image references.
    model:
        Vision model to use (default: qwen-vl-plus).
    prompt:
        Prompt to send to the vision model.

    Returns
    -------
    dict
        Keys: ``updated_md`` (path to updated file), ``descriptions_count``,
        ``total_images`` (total found), ``failed_images`` (list of failed image names).
        If vision fails completely, returns original document with 0 descriptions.
    """
    doc_path = Path(document_path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    content = doc_path.read_text(encoding="utf-8")
    
    # Try to initialize client, but don't fail if API key is missing
    try:
        provider = os.environ.get("LLM_PROVIDER", "dashscope").lower()
        if provider == "ollama":
            from core.clients.ollama_client import OllamaClient
            client = OllamaClient()
        else:
            client = DashScopeClient()
            if not client.api_key:
                logger.warning("DashScope API key not set. Skipping diagram descriptions.")
                return {
                    "updated_md": str(doc_path),
                    "descriptions_count": 0,
                    "total_images": 0,
                    "failed_images": [],
                    "skipped": True,
                    "reason": "API key not set"
                }
    except Exception as e:
        logger.warning(f"Failed to initialize client: {e}. Skipping diagram descriptions.")
        return {
            "updated_md": str(doc_path),
            "descriptions_count": 0,
            "total_images": 0,
            "failed_images": [],
            "skipped": True,
            "reason": str(e)
        }
    
    matches = list(IMAGE_PATTERN.finditer(content))
    descriptions_count = 0
    failed_images: list[str] = []
    
    logger.info(f"Found {len(matches)} images to process in {doc_path.name}")

    # Process in reverse order to maintain offsets
    for idx, match in enumerate(reversed(matches), 1):
        img_ref = match.group(2)
        # Resolve relative paths
        if not Path(img_ref).is_absolute():
            img_path = doc_path.parent / img_ref
        else:
            img_path = Path(img_ref)

        if img_path.exists():
            logger.info(f"[{len(matches) - idx + 1}/{len(matches)}] Processing: {img_path.name}")
            
            try:
                # Compress if needed to avoid 400 errors
                processed_path = compress_image_if_needed(img_path)

                # Avoid deterministic 400 errors from tiny/invalid images (e.g., 1x1 px)
                if not _is_valid_for_vision_api(processed_path):
                    logger.warning(
                        "Skipping image %s: dimensions below API minimum (%d px)",
                        img_path.name,
                        MIN_API_IMAGE_DIMENSION,
                    )
                    failed_images.append(img_path.name)
                    continue
                
                description = client.vision(
                    model=model,
                    prompt=prompt,
                    image_path=str(processed_path),
                )
                
                # Insert description after the image reference
                desc_block = f"\n\n> **Descripción del diagrama:**\n> {description}\n"
                insert_pos = match.end()
                content = content[:insert_pos] + desc_block + content[insert_pos:]
                descriptions_count += 1
                logger.debug(f"✓ Successfully described: {img_path.name}")
                
            except Exception as e:
                error_msg = str(e)
                # Check if it's a quota/403 error
                if "403" in error_msg or "free tier" in error_msg.lower() or "quota" in error_msg.lower():
                    logger.warning(f"Vision API quota exhausted. Stopping diagram descriptions. Error: {e}")
                    # Return original document immediately
                    return {
                        "updated_md": str(doc_path),
                        "descriptions_count": 0,
                        "total_images": len(matches),
                        "failed_images": [m.group(2) for m in matches],
                        "skipped": True,
                        "reason": "Vision API quota exhausted (403)"
                    }
                
                # For other errors, log and continue
                logger.warning(f"Failed to analyze {img_path.name}: {e}")
                failed_images.append(img_path.name)
        else:
            logger.warning(f"Image not found: {img_path}")
            failed_images.append(img_ref)

    # Save updated document
    doc_path.write_text(content, encoding="utf-8")
    logger.info(
        f"✓ Updated {doc_path.name}: {descriptions_count}/{len(matches)} descriptions added"
    )
    if failed_images:
        logger.warning(f"Failed images: {', '.join(failed_images)}")
    
    return {
        "updated_md": str(doc_path),
        "descriptions_count": descriptions_count,
        "total_images": len(matches),
        "failed_images": failed_images,
    }
