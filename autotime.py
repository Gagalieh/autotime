#!/usr/bin/env python3
import requests, time, logging, datetime
from mcstatus import BedrockServer

# ── KONFIGURASI ─────────────────────────────────────────
BEDROCK_HOST  = "shared14.kagestore.xyz"
BEDROCK_PORT  = 19134

PANEL_URL     = "https://dash.kagestore.com"
SERVER_ID     = "bdb20976"
API_KEY       = "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW"

CHECK_INTERVAL = 60  # dalam detik, ubah ke 300 kalau ingin 5 menit
# ────────────────────────────────────────────────────────

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_online_players() -> int:
    try:
        status = BedrockServer.lookup(f"{BEDROCK_HOST}:{BEDROCK_PORT}").status()
        return status.players.online
    except Exception as e:
        logging.error("❌ Gagal ping server Bedrock: %s", e)
        return 0

def send_command(cmd: str):
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/command"
    try:
        r = requests.post(url, headers=HEADERS, json={"command": cmd}, timeout=10)
        if r.status_code == 204:
            logging.info("✔️  Perintah terkirim: %s", cmd)
        else:
            logging.error("❌ Gagal kirim perintah. Status: %s", r.status_code)
    except Exception as e:
        logging.error("❌ Gagal koneksi ke API: %s", e)

def main():
    start = datetime.datetime.now()
    logging.info("⏳ Mulai eksekusi: %s", start.isoformat())

    players = get_online_players()
    if players == 0:
        logging.info("👤 0 pemain online → menghentikan waktu")
        send_command("gamerule doDaylightCycle false")
    else:
        logging.info("🎮 %s pemain online → menyalakan waktu", players)
        send_command("gamerule doDaylightCycle true")

    end = datetime.datetime.now()
    duration = (end - start).total_seconds()
    logging.info("✅ Selesai: %s", end.isoformat())
    logging.info("⏱️ Durasi eksekusi: %.2f detik", duration)

    # Estimasi jika dijalankan setiap CHECK_INTERVAL
    monthly_runs = (60 * 24 * 30) * (60 // CHECK_INTERVAL)
    total_estimated_runtime = monthly_runs * duration / 3600  # dalam jam
    logging.info("📊 Estimasi runtime bulanan: %.2f jam", total_estimated_runtime)

if __name__ == "__main__":
    main()
