import subprocess
import re

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "YouTube Live Channel"
youtube_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"

stream_url = ""

# Mengambil direct URL m3u8 menggunakan yt-dlp dengan format hls/best
try:
    cmd = ["yt-dlp", "-g", "-f", "b/best", youtube_url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    stream_url = res.stdout.strip()
except Exception as e:
    print("Error yt-dlp:", e)

# Fallback ke format proxy manifest jika yt-dlp gagal
if not stream_url or not stream_url.startswith("http"):
    stream_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"

m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{TITLE}",{TITLE}
{stream_url}
"""

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Berhasil update m3u8!")
