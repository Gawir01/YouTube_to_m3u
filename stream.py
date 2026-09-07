import subprocess
import json

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "Official iNews Live"

youtube_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
stream_url = ""

try:
    # Nembak pake player client android biar gak diblokir GitHub Actions
    cmd = [
        "yt-dlp",
        "-g",
        "--extractor-args", "youtube:player_client=android",
        youtube_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    output = res.stdout.strip()
    
    # Ambil baris URL yang valid
    for line in output.split('\n'):
        if "googlevideo.com" in line or ".m3u8" in line:
            stream_url = line
            break
            
    if not stream_url and output.startswith("http"):
        stream_url = output.split('\n')[0]

except Exception as e:
    print("Error:", e)

# Jika gagal, kosongkan agar tidak memicu redirect ke aplikasi YouTube
if "youtube.com/watch" in stream_url:
    stream_url = ""

m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n{stream_url}\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Proses selesai. Stream URL:", stream_url)
