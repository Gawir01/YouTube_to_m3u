import os
import requests

# Masukkan ID Video atau ID Live Stream YouTube (contoh: UMe1AKUyUN0)
# Kamu bisa pakai ID channel live langsung atau ID video tertentu
VIDEO_ID = "UMe1AKUyUN0"
TITLE = "YouTube Live Channel"

# URL manifest M3U8 resmi dari YouTube
stream_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"

# Gunakan format HLS langsung
m3u8_direct_url = f"https://lh3.googleusercontent.com/proxy/yt_live_{VIDEO_ID}" 

# Pilihan terbaik: gunakan format redirect link yt-dlp via URL pihak ketiga atau link m3u8 langsung
# Format standar M3U untuk IPTV player (seperti OTT Navigator)
m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{TITLE}",{TITLE}
https://www.youtube.com/watch?v={VIDEO_ID}
"""

# Jika ingin link direct stream m3u8 langsung tanpa bot block:
# Menggunakan endpoint YouTube hls_manifest_url via scraper cepat
try:
    req = requests.get(f"https://www.youtube.com/watch?v={VIDEO_ID}", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }).text
    
    if "hlsManifestUrl" in req:
        start = req.find("hlsManifestUrl\":\"") + len("hlsManifestUrl\":\"")
        end = req.find("\"", start)
        hls_url = req[start:end].replace("\\/", "/")
        
        m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{TITLE}",{TITLE}
{hls_url}
"""
except Exception as e:
    print("Fallback default link used:", e)

# Simpan ke file playlist.m3u
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

# Simpan ke live_channel.m3u8
with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Playlist generated successfully!")
