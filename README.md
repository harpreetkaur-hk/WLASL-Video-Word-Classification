# WLASL-Video-Word-Classification
A neural network capable of classifying American Sign Language (ASL) words from video input using the WLASL dataset. This project implements deep learning techniques to recognize and output ASL words on the screen, contributing to improved communication accessibility for the deaf community.

## Data

### Data Description:
- Word-Level American Sign Language (WLASL) Dataset.
- Source: https://github.com/dxli94/WLASL
- The WLASL dataset consists of videos depicting various ASL signs, categorized by words.

### Data File Description:
- `WLASL_v0.3.json`: JSON file including all the data samples.
- 2,000 Labels
- 21,083 Video files
- `gloss_video_id.json`

### WLASL_v0.3.json:
- **gloss**: str, data file is structured/categorised based on sign gloss, or namely, labels.
- **fps**: int, frame rate (=25) used to decode the video as in the paper.
- **frame_start**: int, the starting frame of the gloss in the video (decoding with FPS=25), indexed from 1.
- **frame_end**: int, the ending frame of the gloss in the video (decoding with FPS=25). -1 indicates the gloss ends at the last frame of the video.
- **url**: str, used for video downloading.
- **video_id**: str, a unique video identifier.

### gloss_video_id.json:
- It contains 21,083 JSON objects for each video.
- Key is the **video id**.
- Value is **gloss**, **frame_start**, **frame_end**, **url**

### Data Collection
- Referring `gloss_video_id.json` file, `download_youtube_videos.py` script downloads all the youTube videos.
- Downloaded 10,942 videos (Could not download remaining videos because of broken link).

### Data Preprocessing
- `data_preprocessing.py` script preprocess the data:
  - Frame extraction:
    - Taking all raw video files as input from “1-Raw” directory.
    - Extracting frames from each video file.
    - Selecting frames based on **frame_start** and **frame_end** and writing those extracted frames to new video file and storing in “2-Processed” directory.

  - Resizing:
    - Finding the maximum duration (frame_count/frame_rate) from all the videos in “2-Processed” directory and making that as the duration for all the videos.
    - Resizing all the frame height and width to 298 * 298.
    - Storing the videos with same duration, height and width in “4-Final” directory.

- `get_train_val_test_split.py` script splits the data:
  - Videos from “4-Final” directory will be further split into **train**, **val** & **test**.
  - Videos from **train**, **val** & **test** will be used by the Model.

### Data Hierarchy
<img width="671" alt="image" src="https://github.com/user-attachments/assets/b406b19f-c373-4544-be49-a97028dde533" />
