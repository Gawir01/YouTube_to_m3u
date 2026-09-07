import requests

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "YouTube Live Channel"

# Ambil HLS manifest m3u8 langsung dari halaman YouTube
stream_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    html = requests.get(stream_url, headers=headers).text
    
    if "hlsManifestUrl" in html:
        start = html.find("hlsManifestUrl\":\"") + len("hlsManifestUrl\":\"")
        end = html.find("\"", start)
        direct_m3u8 = html[start:end].replace("\\/", "/")
        stream_url = direct_m3u8
except Exception as e:
    print("Gagal mengambil HLS URL:", e)

m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{TITLE}",{TITLE}
{stream_url}
"""

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)
