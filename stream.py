import json
import urllib.request

VIDEO_ID = "UMe1AKUyUN0"
TITLE = "Official iNews Live"

# Menggunakan Invidious Instance publik untuk bypass blokir IP GitHub Actions
INVIDIOUS_INSTANCES = [
    "https://inv.riverside.rocks",
    "https://invidious.nerdvpn.de",
    "https://vid.puffyan.us",
    "https://invidious.flokinet.to",
    "https://invidious.drgns.space"
]

stream_url = ""

for instance in INVIDIOUS_INSTANCES:
    try:
        api_url = f"{instance}/api/v1/videos/{VIDEO_ID}"
        req = urllib.request.Request(
            api_url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Ambil hlsUrl langsung
            hls_url = data.get("hlsUrl")
            if hls_url:
                stream_url = hls_url
                print(f"Berhasil dapet HLS dari {instance}: {stream_url}")
                break
    except Exception as e:
        print(f"Gagal dari {instance}: {e}")
        continue

# Jika tidak nemu hlsUrl khusus, format m3u
if stream_url:
    m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n{stream_url}\n"
else:
    # Jangan isi link youtube.com agar tidak mental
    m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-name=\"{TITLE}\",{TITLE}\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

with open("live_channel.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("Proses selesai!")
