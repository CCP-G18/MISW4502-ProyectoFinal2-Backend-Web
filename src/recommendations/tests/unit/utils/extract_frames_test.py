import os
import shutil
import tempfile
import pytest
import cv2
import numpy as np
from app.utils.extract_frames import extract_frames

@pytest.fixture(scope="module")
def setup_video():
    video_filename = "test_video.avi"

    # Crear un video de 5 segundos a 10 FPS
    frame_width, frame_height = 640, 480
    fps = 10
    duration = 5  # segundos
    total_frames = fps * duration

    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

    for i in range(total_frames):
        # Crear un frame gris con brillo suficiente
        frame = np.full((frame_height, frame_width, 3), 120, dtype=np.uint8)
        out.write(frame)

    out.release()
    yield video_filename

    # Cleanup
    os.remove(video_filename)

def test_extract_frames_should_generate_images(setup_video):
    video_path = setup_video
    with tempfile.TemporaryDirectory() as output_dir:
        extract_frames(video_path, output_dir, num_frames=3)
        extracted_files = os.listdir(output_dir)
        assert len(extracted_files) == 3
        assert all(fname.startswith("frame_") and fname.endswith(".png") for fname in extracted_files)

def test_extract_frames_brightness_filter(setup_video):
    video_path = setup_video
    with tempfile.TemporaryDirectory() as output_dir:
        extract_frames(video_path, output_dir, num_frames=3, min_brightness_threshold=200.0)
        assert len(os.listdir(output_dir)) == 0
