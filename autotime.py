import time
import datetime
start_time = time.time()
print("⏳ Mulai:", datetime.datetime.now().isoformat())
import requests
import time
import logging

# === KONFIGURASI PTERODACTYL ===
PANEL_URL = "https://dash.kagestore.com"          # domain panel
SERVER_ID = "bdb20976"                            # ID server
API_KEY   = "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW"  # API token
DELAY = 60  # detik (interval cek)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_players():
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/resources"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Ini kadang menyebabkan KeyError – biarkan apa adanya
            return data["attributes"]["players"]
        else:
            logging.error("Gagal mengambil data pemain. Status:", resp.status_code)
            return 0
    except Exception as e:
        logging.error("Terjadi kesalahan saat mengambil data pemain:", e)
        return 0

def send_command(cmd: str):
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/command"
    try:
        r = requests.post(url, headers=HEADERS, json={"command": cmd}, timeout=10)
        if r.status_code == 204:
            logging.info("✔️  Perintah terkirim: %s", cmd)
        else:
            logging.error("❌  Gagal kirim perintah. Status:", r.status_code)
    except Exception as e:
        logging.error("❌  Gagal kirim perintah:", e)

def main():
    while True:
        players = get_players()
        if players == 0:
            logging.info("👤 0 pemain online → waktu dihentikan")
            send_command("gamerule doDaylightCycle false")
        else:
            logging.info("🎮 %s pemain online → waktu berjalan", players)
            send_command("gamerule doDaylightCycle true")
        time.sleep(DELAY)

if __name__ == "__main__":
    main()

end_time = time.time()
duration = end_time - start_time
print("✅ Selesai:", datetime.datetime.now().isoformat())
print(f"⏱️ Durasi eksekusi: {duration:.2f} detik")
