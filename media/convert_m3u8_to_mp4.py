import os
import re
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
def process_directory(base_directory, video_uri_filter, audio_uri_filter):
    for root, dirs, files in os.walk(base_directory):
        if 'done' in root:
            # adds an option to prefix 'done' to any directories that you want skipped
            print('skipping', root)
            continue
        for file in files:
            if file.endswith(".m3u8"):
                file_path = os.path.join(root, file)
                video_uri, audio_uri = extract_uris(file_path, video_uri_filter, audio_uri_filter)
                output_name = os.path.splitext(file)[0]
                print('output is', output_name)
                if audio_uri and video_uri:
                    audio_output = f"{output_name}_audio.mp4"
                    audio_command = [
                        "ffmpeg", "-i", audio_uri, "-vn", "-acodec", "copy", audio_output
                    ]
                    print(f"Downloading audio to {audio_output}...")
                    subprocess.run(audio_command, check=True)

                    video_output = f"{output_name}_video.mp4"
                    video_command = [
                        "ffmpeg", "-i", video_uri, "-an", "-vcodec", "copy", video_output
                    ]
                    print(f"Downloading video to {video_output}...")
                    subprocess.run(video_command, check=True)

                    # merge the audio and video streams into a single file
                    combined_output = f"{output_name}.mp4"
                    merge_command = [
                        "ffmpeg", "-i", f"{audio_output}", "-i", f"{video_output}", "-c", "copy", combined_output
                    ]
                    print(f"Merging audio and video into {combined_output}...")
                    subprocess.run(merge_command, check=True)
                    print(f"Combined file saved as {combined_output}.")
                    
                    print("Removing intermediate files...")
                    try:
                        print(f"Deleting {audio_output}...")
                        os.remove(audio_output)
                        print(f"Deleting {video_output}...")
                        os.remove(video_output)
                    except OSError as e:
                        print(f"Error while deleting files: {e}")
                else:
                    print("URIs not scraped. Please ensure both audio and video URIs are set")



if __name__ == "__main__":
    # base_directory should be the top level of your folder strucutre where your list of m3u8 files are saved.
    # could also be a flat directory with all your m3u8 files in your base_directory
    # e.g. 
    # top_level
    #..subdir0
    #....subdir1
    #........myfile.m3u8
    #....subdir2
    #........myfile2.m3u8
    base_directory = "dir_containing_your_m3u8_files"
    video_uri_filter = "RESOLUTION=1920x1080" # can be any keyword you want to target from the m3u8 file that is specific to the video url you want
    audio_uri_filter = 'GROUP-ID="audio-high"' # can be any keyword you want to target from the m3u8 file that is specific to the audio url you want
    process_directory(base_directory, video_uri_filter, audio_uri_filter)
