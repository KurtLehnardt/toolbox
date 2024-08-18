import os
import re
import time
import subprocess


# Function to extract video and audio URIs from m3u8 files
def extract_uris(file_path, video_uri_filter, audio_uri_filter):
    video_uri = None
    audio_uri = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # Check for the video URI with the specified resolution
            if video_uri_filter in line:
                if i + 1 < len(lines):
                    video_uri = lines[i + 1].strip()
            # Check for the audio URI with the specified group-id
            if audio_uri_filter in line:
                audio_match = re.search(r'URI="(.*?)"', line)
                if audio_match:
                    audio_uri = audio_match.group(1)
    return video_uri, audio_uri

# Function to traverse directories and process m3u8 files
def process_directory(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'done' in root:
            # adds an option to prefix 'done' to any directories that you want skipped
            print('skipping', root)
            continue
        for file in files:
            if file.endswith(".m3u8"):
                file_path = os.path.join(root, file)
                video_uri, audio_uri = extract_uris(file_path)
                if video_uri and audio_uri:
                    new_filename = os.path.splitext(file)[0] + '_' + str(time.time()) + "_combined.mp4"
                    output_file_path = os.path.join(root, new_filename)
                    output_dir = os.path.dirname(output_file_path)
                    os.makedirs(output_dir, exist_ok=True)
                    ffmpeg_command = [
                        "ffmpeg",
                        "-i", video_uri,
                        "-i", audio_uri,
                        "-bsf:a", "aac_adtstoasc",
                        "-vcodec", "copy",
                        "-c", "copy",
                        "-crf", "50",
                        output_file_path
                    ]
                    try:
                        subprocess.run(ffmpeg_command, check=True, shell=True)
                    except subprocess.CalledProcessError as e:
                        print(f"failed to execute ffmpeg command for {video_uri}", "\n", "error: {e}", "\n")
                else:
                    print("URIs not scraped. Please ensure both audio and video URIs are set")



if __name__ == "__main__":
    # base_directory should be the top level of your folder strucutre where your list of m3u8 files are saved.
    # e.g. 
    # top_level
    #..subdir0
    #....subdir1
    #........myfile.m3u8
    #....subdir2
    #........myfile2.m3u8
    base_directory = "workouts"
    video_uri_filter = "RESOLUTION=1920x1080" # can be any keyword you want to target from the m3u8 file that is specific to the video url you want
    audio_uri_filter = 'GROUP-ID="audio-high"' # can be any keyword you want to target from the m3u8 file that is specific to the audio url you want
    process_directory(base_directory, video_uri_filter, audio_uri_filter)


