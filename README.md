# Video Processing & Inference Project
This project is focused on human detection. It includes scripts for extracting frames, drawing zones, and running inference on video streams.
# 📂 Project Structure

```sh
├── assets
│   ├── models  #store model weights
│   └── videos
│       ├── input # Input videos
│       └── processed # Processed videos
├── scripts # Utility scripts for video processing
│   ├── draw_zones.py
│   ├── extract_frames.py
│   ├── stream_utils # Streaming-related utilities
│   │   └── stream_from_file.py
│   └── video_processing # Video transformation scripts
│       └── rotate_video.py
├── src # Core source code
│   ├── inference # Scripts for video analysis with `inference`
│   │   ├── basic_inference.py
│   │   ├── naive_stream_inference.py
│   │   └── stream_inference.py
│   ├── ultralytics # Scripts for video analysis with `ultralytics`
│   │   ├── basic_ultralytics.py
│   │   ├── naive_stream_ultralytics.py
│   │   └── stream_ultralytics.py
│   └── utils # General utility functions
│       ├── clocks.py
│       ├── general.py
│       ├── __init__.py
└── zones # Store zone configuration files
```
