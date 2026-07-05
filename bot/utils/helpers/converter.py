import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)

FFMPEG_TIMEOUT = 60  # secondes, limite de securite pour le subprocess


class ConversionError(Exception):
    pass


def _run_ffmpeg(args):
    logger.debug('running ffmpeg: %s', ' '.join(args))
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=FFMPEG_TIMEOUT
    )
    if result.returncode != 0:
        logger.error('ffmpeg error: %s', result.stderr.decode(errors='ignore'))
        raise ConversionError('ffmpeg failed with code {}'.format(result.returncode))


def convert_image_to_webp(input_path: str, output_tempfile):
    """convertit une photo (jpg/png/...) en sticker statique webp 512x512"""
    with tempfile.NamedTemporaryFile(suffix='.webp', delete=False) as tmp_out:
        output_path = tmp_out.name

    try:
        _run_ffmpeg([
            'ffmpeg', '-y', '-i', input_path,
            '-vf', 'scale=512:512:force_original_aspect_ratio=decrease,'
                   'pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000',
            '-vcodec', 'libwebp',
            '-lossless', '0',
            '-q:v', '90',
            '-preset', 'picture',
            output_path
        ])

        with open(output_path, 'rb') as f:
            output_tempfile.write(f.read())
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def convert_video_to_webm(input_path: str, output_tempfile):
    """convertit une video/gif en sticker video conforme a Telegram
    (webm, vp9, <= 3 secondes, 512x512, sans audio)"""
    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp_out:
        output_path = tmp_out.name

    try:
        _run_ffmpeg([
            'ffmpeg', '-y', '-i', input_path,
            '-t', '3',  # Telegram: sticker video max 3 secondes
            '-vf', 'scale=512:512:force_original_aspect_ratio=decrease,'
                   'pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000,fps=30',
            '-c:v', 'libvpx-vp9',
            '-b:v', '256k',
            '-crf', '30',
            '-an',  # pas d'audio, obligatoire pour Telegram
            output_path
        ])

        with open(output_path, 'rb') as f:
            output_tempfile.write(f.read())
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
