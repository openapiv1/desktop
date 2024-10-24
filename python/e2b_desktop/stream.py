code = """
import mux_python
from mux_python.rest import ApiException
import subprocess
import time

# Configure Mux API client
configuration = mux_python.Configuration()
configuration.username = 'b8b2ff56-6170-4df9-b9c9-bd4b0cbd947b'
configuration.password = 'vPclncUMEubKlQg4upDPslCNxjAHI7JN7pO34q/0lSHjb+oQAktpVD22D0HRZJ1YnZoAxjzsDYt'

# Create an instance of the API class
api_instance = mux_python.LiveStreamsApi(mux_python.ApiClient(configuration))

# Create a new live stream
create_asset_request = mux_python.CreateAssetRequest(
    playback_policy=[mux_python.PlaybackPolicy("PUBLIC")]
)
create_live_stream_request = mux_python.CreateLiveStreamRequest(
    playback_policy=[mux_python.PlaybackPolicy("PUBLIC")],
    new_asset_settings=create_asset_request
)

try:
    # Create the live stream
    api_response = api_instance.create_live_stream(create_live_stream_request)
    stream_key = api_response.stream_key
    playback_id = api_response.playback_ids[0].id

    print(f"Stream Key: {stream_key}")
    print(f"Playback ID: {playback_id}")

    # FFmpeg command to stream video (replace with your video file path)
    ffmpeg_command = [
        'ffmpeg',
        '-re',  # Read input at native frame rate
        '-i', '/path/to/your/video.mp4',  # Replace with your video file path
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-c:a', 'aac',
        '-f', 'flv',
        f'rtmp://global-live.mux.com:5222/app/{stream_key}'
    ]

    # Start streaming
    process = subprocess.Popen(ffmpeg_command)

    # Stream for a certain duration (e.g., 60 seconds)
    time.sleep(60)

    # Stop streaming
    process.terminate()

except ApiException as e:
    print("Exception when calling LiveStreamsApi->create_live_stream: %s\n" % e)
"""
