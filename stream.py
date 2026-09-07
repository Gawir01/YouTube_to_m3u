import requests
import re

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "YouTube Live Channel"

url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

stream_url = url

try:
    response = requests.get(url, headers=headers)
    html = response.text
    
    # Cari URL HLS manifest m3u8 dari YouTube
    match = re.search(r'hlsManifestUrl":"([^"]+)"', html)
    if match:
        stream_url = match.group(1).replace(r'\/', '/')
        print("HLS URL ditemukan:", stream_url)
    else:
        print("HLS URL tidak ditemukan, menggunakan URL fallback.")
except Exception as e:
    print("Error:", e)

m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{TITLE}",{TITLE}
{stream_url}
"""

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Selesai memperbarui playlist!")
