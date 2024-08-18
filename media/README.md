# Content Description

## convert_m3u8_to_mp4.py
- this script takes a directory structure of m3u8 files that contain both to audio and video URIs, and uses ffmpeg to download the corresponding audio and video files and combine them into a single mp4 video.

- Here is an example .m3u8 file, where the audio URIs are single line comments, and the video URIs are described by the comments on the line above them.
```
#EXTM3U
#EXT-X-STUFF
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-low",NAME="Original",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="https://my-cool-cdn.com/12345/audio/playlist.m3u8"
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-high",NAME="Original",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="https://my-cool-cdn.com/23456/audio/playlist.m3u8"

#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=4987004,AVERAGE-BANDWIDTH=4300000,RESOLUTION=1920x1080,FRAME-RATE=29.970,CODECS="avc1.640028,mp4a.40.2",AUDIO="audio-high"
https://my-cool-cdn.com/12345/video/playlist.m3u8
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=672434,AVERAGE-BANDWIDTH=544000,RESOLUTION=640x360,FRAME-RATE=29.970,CODECS="avc1.64001E,mp4a.40.2",AUDIO="audio-low"
https://my-cool-cdn.com/23456/video/playlist.m3u8
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=2429137,AVERAGE-BANDWIDTH=2070000,RESOLUTION=1280x720,FRAME-RATE=29.970,CODECS="avc1.640020,mp4a.40.2",AUDIO="audio-high"
https://my-cool-cdn.com/34567/video/playlist.m3u8
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=1399221,AVERAGE-BANDWIDTH=1162000,RESOLUTION=960x540,FRAME-RATE=29.970,CODECS="avc1.64001F,mp4a.40.2",AUDIO="audio-low"
https://my-cool-cdn.com/45678/video/playlist.m3u8
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=363069,AVERAGE-BANDWIDTH=293000,RESOLUTION=426x240,FRAME-RATE=29.970,CODECS="avc1.640015,mp4a.40.2",AUDIO="audio-low"
https://my-cool-cdn.com/56789/video/playlist.m3u8
```
