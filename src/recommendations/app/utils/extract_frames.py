import os
import cv2

def extract_frames(video_path, output_dir, num_frames, min_brightness_threshold = 40.0):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps

    print(f"📽️ Duración del video: {duration:.2f} segundos, FPS: {fps}, Total frames: {total_frames}")

    interval = duration / (num_frames + 1)

    extracted = 0
    current_sec = interval

    while extracted < num_frames:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_sec * 1000)
        ret, frame = cap.read()

        if not ret:
            print(f"⚠️ Frame no leído en segundo {current_sec}")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        if brightness >= min_brightness_threshold:
            frame_path = os.path.join(output_dir, f"frame_{extracted}.png")
            cv2.imwrite(frame_path, frame)
            print(f"✅ Frame {extracted} extraído en segundo {current_sec:.2f} (brillo: {brightness:.2f})")
            extracted += 1
        else:
            print(f"🔄 Frame descartado por brillo bajo ({brightness:.2f})")

        current_sec += interval

    cap.release()
    print(f"📸 Total de frames guardados: {extracted}")