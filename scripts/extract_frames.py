import os
import subprocess
from pathlib import Path
from tqdm import tqdm
import argparse
from concurrent.futures import ProcessPoolExecutor
import cv2


def make_parser():
    """
    Create argument parser for the script.
    """
    parser = argparse.ArgumentParser(description="Extract frames from video files.")
    parser.add_argument(
        "-p", "--path", type=str, required=True,
        help="Path to the folder containing video files."
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True,
        help="Path to the folder to save extracted frames."
    )
    parser.add_argument(
        "-n", "--num-processes", type=int, default=4,
        help="Number of parallel processes to use. Default is 4."
    )
    return parser.parse_args()


def get_video_fps(video_path):
    """
    Retrieve the FPS (frames per second) of a video file.
    """
    try:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        return int(fps) if fps > 0 else 30  # Default to 30 FPS if unable to retrieve
    except Exception as e:
        print(f"[ERROR] Unable to retrieve FPS for {video_path}: {e}")
        return 30  # Fallback to 30 FPS


def extract_frames(video_file, output_folder, file_headname, fps):
    """
    Extract frames from a video file using ffmpeg.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        output_pattern = os.path.join(output_folder, f"{file_headname}_%06d.jpg")
        command = [
            "ffmpeg",
            "-i", str(video_file),
            "-r", str(fps),
            "-q:v", "2",  # Quality level (lower is better)
            "-f", "image2",
            output_pattern,
            "-hide_banner",
            "-loglevel", "error"
        ]
        subprocess.run(command, check=True)
        print(f"[INFO] Frames extracted for {video_file} into {output_folder}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Frame extraction failed for {video_file}: {e}")


def process_video(video_path, output_base_path):
    """
    Process a single video file: determine FPS and extract frames.
    """
    try:
        # Determine FPS of the video
        fps = get_video_fps(video_path)
        print(f"[INFO] Detected FPS for {video_path}: {fps}")
        
        # Define the output folder structure based on the video file path
        relative_path = video_path.relative_to(Path(output_base_path).parent)
        output_folder = Path(output_base_path) / relative_path.parent
        file_headname = video_path.stem  # File name without extension
        
        # Extract frames
        extract_frames(video_path, output_folder, file_headname, fps)
    except Exception as e:
        print(f"[ERROR] Failed to process video {video_path}: {e}")


def main(path, output_folder, num_processes):
    """
    Main function to process all video files in the specified directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    print(f"[INFO] Output directory set to: {output_folder}")

    # Search for video files
    videos = list(Path(path).rglob("*.mp4")) + list(Path(path).rglob("*.avi"))
    if not videos:
        print(f"[WARNING] No video files found in the specified path: {path}")
        return

    print(f"[INFO] Found {len(videos)} video(s) in the directory. Starting frame extraction...")
    
    # Process videos with parallel execution
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        list(tqdm(
            executor.map(process_video, videos, [output_folder] * len(videos)),
            total=len(videos),
            desc="Processing Videos"
        ))

    print("[INFO] Frame extraction completed successfully!")


if __name__ == "__main__":
    args = make_parser()
    
    # Display start message
    print("[INFO] Starting the frame extraction process...")
    print(f"[INFO] Input Path: {args.path}")
    print(f"[INFO] Output Path: {args.output}")
    print(f"[INFO] Using {args.num_processes} parallel processes.")
    
    # Execute the main function
    main(args.path, args.output, args.num_processes)
