from pytube import YouTube
import json
import os

def download_youtube_video(data, output_folder):
	"""
	Downloads a YouTube video to the specified output folder.
	Args:
	url (str): The URL of the YouTube video to download.
	output_folder (str): The path to the output folder where the video will be saved.
	"""
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	
	for video_id, video_info in data.items():
		url = video_info["url"]
		if "youtube" in url or "youtu.be" in url:
			try:
				yt = YouTube(url)
				video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
				output_filename = f"{video_id}.mp4"
				video.download(output_folder, filename=output_filename)
				print(f"Video downloaded: {url}  {output_filename}")
			except:
				print(f"Video unavailable: {url}")

if __name__ == "__main__":

	with open('gloss_video_id.json', 'r') as file:
		data = json.load(file)

	output_folder = "./Dataset/1-Raw"
	download_youtube_video(data, output_folder)
	print("Videos are downloaded successfully")

