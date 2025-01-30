import cv2
import argparse

def rotate_video(input_video_path, output_video_path):
    # Capture the original video
    cap = cv2.VideoCapture(input_video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video.")
        return

    # Get total number of frames, width, height, and FPS of the input video
    frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Open the output video file with the same FPS and frame size
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    newvideoR = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    print(f"Processing video: {input_video_path}")
    print(f"Total frames: {frame_number}, FPS: {fps}, Resolution: {frame_width}x{frame_height}")

    # Loop through each frame
    for i in range(frame_number):
        ret, frame = cap.read()
        
        if not ret:
            print(f"Error: Couldn't read frame {i}")
            break

        # Rotate the frame by 180 degrees
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Show the rotated frame (optional)
        cv2.imshow('Rotated Video', rotated_frame)
        
        # Write the rotated frame to the output video
        newvideoR.write(rotated_frame)

        # If the user presses 'q', exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video objects and close any OpenCV windows
    cap.release()
    newvideoR.release()
    cv2.destroyAllWindows()
    print(f"Output video saved as {output_video_path}")

def main():
    # Argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description="Rotate a video by 180 degrees and preserve original FPS.")
    parser.add_argument("--input_video", type=str, help="Path to the input video file.")
    parser.add_argument("--output_video", type=str, help="Path to save the rotated output video.")
    args = parser.parse_args()

    # Call the rotate_video function with arguments
    rotate_video(args.input_video, args.output_video)

if __name__ == "__main__":
    main()
