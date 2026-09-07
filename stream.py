import urllib.request
import re

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "Official iNews Live"

url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

req = urllib.request.Request(url, headers=headers)
stream_url = ""

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        # Cari URL HLS Manifest m3u8 asli dari halaman YouTube
        matches = re.findall(r'https%3A%2F%2Fmanifest.googlevideo.com%2Fapi%2Fmanifest%2Fhls_variant%2F[^\s"\'<>]+', html)
        if not matches:
            matches = re.findall(r'https://manifest.googlevideo.com/api/manifest/hls_variant/[^\s"\'<>]+', html)
        
        if matches:
            stream_url = urllib.parse.unquote(matches[0]).replace('\\/', '/')
            print("Berhasil menemukan link HLS:", stream_url)
        else:
            print("Gagal mengekstrak HLS manifest.")
except Exception as e:
    print("Error saat request:", e)

# Jika gagal, jangan gunakan fallback link youtube.com biasa agar tidak mentall
m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n{stream_url}\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)
