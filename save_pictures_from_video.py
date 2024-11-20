import os
import subprocess
import sys
import platform

# List of video file extensions to look for
video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg', '.webm', '.3gp']

# Determine the ffmpeg executable based on the operating system
if platform.system() == 'Windows':
    ffmpeg_executable = 'ffmpeg.exe'
else:
    ffmpeg_executable = 'ffmpeg'

# Function to check if ffmpeg is available
def is_ffmpeg_available():
    try:
        subprocess.run([ffmpeg_executable, '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

if not is_ffmpeg_available():
    print("FFmpeg is not installed or not found in PATH.")
    print("Please install FFmpeg and ensure it's added to your system's PATH.")
    sys.exit(1)

# Walk through all directories and subdirectories
for root, dirs, files in os.walk('.'):
    for file in files:
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_path = os.path.join(root, file)
            video_name = os.path.splitext(file)[0]
            output_folder = os.path.join(root, f'{video_name} - pictures')

            # Create the output directory if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Define the output file pattern
            output_pattern = os.path.join(output_folder, 'image%04d.png')

            # Build the ffmpeg command
            command = [
                ffmpeg_executable,
                '-i', video_path,
                '-vf', 'fps=1',
                output_pattern
            ]

            # Run the ffmpeg command
            print(f'Processing video: {video_path}')
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f'Error processing {video_path}: {e}')
