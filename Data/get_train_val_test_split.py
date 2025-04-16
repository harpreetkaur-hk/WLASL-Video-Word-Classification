import os
import json
import shutil

# Load the JSON data
with open('../gloss_video_id.json', 'r') as f:
    data = json.load(f)

# Set the directory where the videos are located
video_dir = r"./Dataset/4-Final"
final_dir = r"./Dataset/Finally"

# Iterate through the videos in the directory
counter = 0
for filename in os.listdir(video_dir):
    if filename.endswith('.mp4'):
        video_id = os.path.splitext(filename)[0]
        if video_id in data:
            gloss = data[video_id]['gloss']
            
            # Create the folder for the gloss if it doesn't exist
            gloss_dir = os.path.join(video_dir, gloss)
            if not os.path.exists(gloss_dir):
                os.makedirs(gloss_dir)
            
            # Move the video to the gloss folder
            src_path = os.path.join(video_dir, filename)
            dst_path = os.path.join(gloss_dir, filename)
            if (os.path.exists(dst_path)):
                counter = counter + 1
            else:
                shutil.move(src_path, dst_path)
                print(f"Moved {filename} to {gloss_dir}")
        else:
            print(f"Video ID {video_id} not found in the JSON data.")

def count_non_hidden_files(directory):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        # Filter out hidden files
        files = [f for f in files if not f.startswith('.')]
        # Filter out hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        total_files += len(files)
    return total_files

# Specify the directory you want to search

# Count non-hidden files
file_count = count_non_hidden_files(video_dir)
print(f"Total non-hidden files: {file_count}")

# Count the total no. of videos for each gloss and create train, val and test datasets
for gloss_dir in os.listdir(video_dir):
	counter = 0
	if not gloss_dir.startswith('.'):
		video_files = [file for file in os.listdir(os.path.join(video_dir, gloss_dir)) if file.endswith(".mp4")]
		for vid in video_files:
			if vid.endswith('.mp4'):
				counter = counter + 1
		print(f"gloss: {gloss_dir}, total videos: {counter}")
		if counter >= 15:
			# Create the 'train', 'val', and 'test' folders if they don't exist
			for folder in ['train', 'val', 'test']:
				folder_path = os.path.join(final_dir, folder)
				if not os.path.exists(folder_path):
					os.makedirs(folder_path)
            
			# Create the folder for the gloss if it doesn't exist
			train_gloss_dir = os.path.join(final_dir, 'train', gloss_dir)
			if not os.path.exists(train_gloss_dir):
				os.makedirs(train_gloss_dir)
			val_gloss_dir = os.path.join(final_dir, 'val', gloss_dir)
			if not os.path.exists(val_gloss_dir):
				os.makedirs(val_gloss_dir)
			test_gloss_dir = os.path.join(final_dir, 'test', gloss_dir)
			if not os.path.exists(test_gloss_dir):
				os.makedirs(test_gloss_dir)

			# Copy the first 3 videos to the 'train' folder
			for i, video_file in enumerate(video_files):
				if i < 13:
					src_path = os.path.join(video_dir, gloss_dir, video_file)
					dst_path = os.path.join(train_gloss_dir, video_file)
					shutil.copy(src_path, dst_path)
				elif i == 13:
					src_path = os.path.join(video_dir, gloss_dir, video_file)
					dst_path = os.path.join(val_gloss_dir, video_file)
					shutil.copy(src_path, dst_path)
				elif i == 14:
					src_path = os.path.join(video_dir, gloss_dir, video_file)
					dst_path = os.path.join(test_gloss_dir, video_file)
					shutil.copy(src_path, dst_path)

