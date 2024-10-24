from mux_python.rest import ApiException
import subprocess
import time


import os
import sys
import time
import mux_python
from mux_python.rest import NotFoundException

# Configure Mux API client
configuration = mux_python.Configuration()
configuration.username = 'b8b2ff56-6170-4df9-b9c9-bd4b0cbd947b'
configuration.password = 'vPclncUMEubKlQg4upDPslCNxjAHI7JN7pO34q/0lSHjb+oQAktpVD22D0HRZJ1YnZoAxjzsDYt'

# API Client Initialization
live_api = mux_python.LiveStreamsApi(mux_python.ApiClient(configuration))
playback_ids_api = mux_python.PlaybackIDApi(mux_python.ApiClient(configuration))

# ========== create-live-stream ==========
new_asset_settings = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
create_live_stream_request = mux_python.CreateLiveStreamRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC], new_asset_settings=new_asset_settings)
create_live_stream_response = live_api.create_live_stream(create_live_stream_request)
assert create_live_stream_response != None
assert create_live_stream_response.data != None
assert create_live_stream_response.data.id != None

stream_key = create_live_stream_response.data.stream_key
playback_id = create_live_stream_response.data.playback_ids[0].id
print(stream_key)
print(playback_id)
print("create-live-stream OK �[m~\~E")

try:
    print(f"Stream Key: {stream_key}")
    print(f"Playback ID: {playback_id}")

    # FFmpeg command to stream video (replace with your video file path)
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'x11grab',  # Capture from X11 display (screen)
        '-s', '1024x768',  # Set the size of the capture (adjust as needed)
        '-i', ':99',  # Capture from the main display
        #'-f', 'alsa',  # Audio input format
        #'-i', 'default',  # Default audio device
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        #'-c:a', 'aac',
        '-f', 'flv',
        f'rtmp://global-live.mux.com:5222/app/{stream_key}'
    ]
    # ffmpeg_command = [
    #     'ffmpeg',
    #     '-re',  # Read input at native frame rate
    #     '-i', '/home/user/video.mp4',  # Replace with your video file path
    #     '-c:v', 'libx264',
    #     '-preset', 'veryfast',
    #     '-c:a', 'aac',
    #     '-f', 'flv',
    #     f'rtmp://global-live.mux.com:5222/app/{stream_key}'
    # ]

    # Start streaming
    process = subprocess.Popen(ffmpeg_command)

    # Stream for a certain duration (e.g., 60 seconds)
    time.sleep(60)

    # Stop streaming
    process.terminate()

except ApiException as e:
    print("Exception when calling LiveStreamsApi->create_live_stream: %s\n" % e)