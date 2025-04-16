import os
import cv2
import json
from math import ceil

input_directory = r"./Dataset/1-Raw"
extracted_directory = r"./Dataset/2-Processed"
output_directory = r"./Dataset/3-Processed"
new_output_directory = r"./Dataset/4-Final"
#frame_rate = 25

def get_video_properties(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties: duration, frame count, width, height, frame rate
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / frame_rate
    
    # Release the video capture object
    cap.release()
    
    # print("--------------------------")
    # print(f"VideoPath: {video_path}")
    # print(f"duration: {duration}")
    # print(f"frame_count: {frame_count}")
    # print(f"frame_rate: {frame_rate}")
    
    return duration, frame_rate, width, height, frame_count


def video_to_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    
    if not cap.isOpened:
        print(f"Error opening video stream or file: {video_path}")
        return []
    frames = []
    isFirst = False
    while True:
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            break
    cap.release()
    return frames, width, height, frame_rate


def extract_frame_as_video(content):
	video_files = [file for file in os.listdir(input_directory) if file.endswith(".mp4")]
	
	for video_file in video_files:
		frame_start = content[video_file.split('.')[0]]["frame_start"] -1
		frame_end = content[video_file.split('.')[0]]["frame_end"] - 1
        
		result = video_to_frames(os.path.join(input_directory,video_file))
		outframes = result[0][frame_start:frame_end + 1]
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(extracted_directory+ '/' + video_file, fourcc, 25,(result[1],result[2]))
		
		for i in range(len(outframes)):
			out.write(outframes[i])
		out.release()


def standardize_video_properties(input_dir, output_dir):
    
    # Get a list of all video files in the input directory
    video_files = [file for file in os.listdir(input_dir) if file.endswith(".mp4")]
    
    # Find the video with the longest duration and largest frame size
    max_duration = 0
    max_width = 299
    max_height = 299
    
    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        duration, _, width, height, _ = get_video_properties(video_path)
        if duration > max_duration:
            max_duration = duration
    
    # Standardize the duration and frame size of all videos
    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        duration, frame_rate, width, height, _ = get_video_properties(video_path)
        
        # Calculate the number of frames to skip or duplicate to match the longest duration
        target_frames = int(max_duration * frame_rate)
        current_frames = int(duration * frame_rate)
        ratio = target_frames / current_frames
        
        # Open the input video file
        cap = cv2.VideoCapture(video_path)
        
        # Create VideoWriter object for output with the maximum width and height
        output_path = os.path.join(output_dir, video_file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, (max_width, max_height))
        
        # Read frames and write them to output video
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize frame to match the maximum width and height
            frame_resized = cv2.resize(frame, (max_width, max_height))
            # Write the same frame multiple times if the video is shorter
            for _ in range(int(ratio)):
                out.write(frame_resized)
            
        cap.release()
        out.release()
        
        duration, frame_rate, width, height, _ = get_video_properties(output_path)
        
        # Calculate the number of frames to skip or duplicate to match the longest duration
        target_frames = int(max_duration * frame_rate)
        current_frames = int(duration * frame_rate)
        ratio = target_frames / current_frames
        
        # Release VideoCapture and VideoWriter objects
        new_frame_count = int(ratio) * current_frames
        leftover = target_frames - new_frame_count
        
        print(f"new_frame_count: {new_frame_count}")
        print(f"leftover: {leftover}")
        
        output1_path = os.path.join(new_output_directory, video_file)
        cap = cv2.VideoCapture(output_path)
        out = cv2.VideoWriter(output1_path, fourcc, frame_rate, (max_width, max_height))
        
        counter = 0
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if counter > new_frame_count - 1 :
                 break
                 
            out.write(frame)
            counter = counter + 1
            
            if leftover != 0:
                out.write(frame)
                leftover = leftover - 1
            
        cap.release()
        out.release()
        
        duration, frame_rate, width, height, frame_count = get_video_properties(output1_path)
        print(duration, frame_rate,width,height, frame_count)
    
    # Get a list of all video files in the input directory
    video_files = [file for file in os.listdir(extracted_directory) if file.endswith(".mp4")]
    
    # Find the video with the longest duration and largest frame size
    max_duration = 0
    max_width = 299
    max_height = 299
        
    for video_file in video_files:
        video_path = os.path.join(extracted_directory, video_file)
        duration, _, width, height, _ = get_video_properties(video_path)
        if duration > max_duration:
            max_duration = duration
    
    target_frames = int(max_duration * 25)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #print(f"target_frames: {target_frames}")
    
    # Standardize the duration and frame size of all videos
    for video_file in video_files:
        output_path = os.path.join(output_directory,video_file)
        
        if os.path.exists(output_path):
            continue
        
        extracted_path = os.path.join(extracted_directory,video_file)
        duration, frame_rate, width, height, _ = get_video_properties(extracted_path)
        
         # Calculate the number of frames to skip or duplicate to match the longest duration
        current_frames = int(duration * frame_rate)
        #print(f"current_frames: {current_frames}")
        ratio = target_frames / current_frames
        #print(f"ratio: {ratio}")
        
        cap = cv2.VideoCapture(extracted_path)
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, (max_width, max_height))
        
        # Read frames and write them to output video
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize frame to match the maximum width and height
            frame_resized = cv2.resize(frame, (max_width, max_height))
            # Write the same frame multiple times if the video is shorter
            for _ in range(int(ratio)):
                out.write(frame_resized)
        
        cap.release()
        out.release()
        
        duration, frame_rate, width, height, _ = get_video_properties(output_path)
        
        # Calculate the number of frames to skip or duplicate to match the longest duration
        current_frames = int(duration * frame_rate)
        #print(f"current_frames: {current_frames}")
        ratio = target_frames / current_frames
        #print(f"ratio: {ratio}")
            
        # Release VideoCapture and VideoWriter objects
        new_frame_count = int(ratio) * current_frames
        leftover = target_frames - new_frame_count
        
        cap = cv2.VideoCapture(output_path)
        output1_path = os.path.join(new_output_directory, video_file)
        out = cv2.VideoWriter(output1_path, fourcc, frame_rate, (max_width, max_height))
        
        counter = 0
        while True:
            ret, frame = cap.read()
            print(f"frame shape: {frame.shape}")
            
            if not ret:
                break
            
            if counter > new_frame_count - 1 :
                 break
                 
            out.write(frame)
            counter = counter + 1
            
            if leftover != 0:
                out.write(frame)
                leftover = leftover - 1
            
        cap.release()
        out.release()
        
        duration, indv_frame_rate, width, height, frame_count = get_video_properties(output1_path)
        print(duration, indv_frame_rate,width,height, frame_count)
    

if __name__ == "__main__":
	
	content = json.load(open('gloss_video_id.json'))
	extract_frame_as_video(content)
	standardize_video_properties(extracted_directory, output_directory)
