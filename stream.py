import json
import urllib.request
import re

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "Official iNews Live"

stream_url = ""

try:
    # 1. Tembak halaman embed YouTube untuk mengambil manifest HLS m3u8
    embed_url = f"https://www.youtube.com/embed/{VIDEO_ID}"
    req = urllib.request.Request(
        embed_url, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        
        # Cari URL hlsManifestUrl / googlevideo.com di dalam kode JS embed
        match = re.search(r'\"hlsManifestUrl\":\"(https:[^\"]+)\"', html)
        if match:
            stream_url = match.group(1).replace("\\/", "/")
            print("Berhasil menemukan hlsManifestUrl:", stream_url)

    # 2. Jika tidak ketemu di embed, gunakan Innertube Android API langsung
    if not stream_url:
        api_url = "https://www.youtube.com/youtubei/v1/player"
        payload = json.dumps({
            "videoId": VIDEO_ID,
            "context": {
                "client": {
                    "clientName": "ANDROID",
                    "clientVersion": "19.02.39"
                }
            }
        }).encode('utf-8')
        
        api_req = urllib.request.Request(
            api_url, 
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(api_req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hls_url = data.get("streamingData", {}).get("hlsManifestUrl")
            if hls_url:
                stream_url = hls_url
                print("Berhasil menemukan HLS via Innertube API:", stream_url)

except Exception as e:
    print("Error:", e)

# Susun isi M3U
if stream_url:
    m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n{stream_url}\n"
else:
    # Jika gagal total, jangan isi link agar tidak melempar aplikasi
    m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Proses Selesai. Hasil URL:", stream_url)
