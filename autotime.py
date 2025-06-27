#!/usr/bin/env python3
import requests, time, logging, datetime
from mcstatus import BedrockServer

# ── CONFIG ─────────────────────────────────────────
BEDROCK_HOST  = "shared14.kagestore.xyz"
BEDROCK_PORT  = 19134

PANEL_URL     = "https://dash.kagestore.com"
SERVER_ID     = "bdb20976"
API_KEY       = "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW"

CHECK_INTERVAL = 60           # detik (loop setiap 60 s)
# ──────────────────────────────────────────────────

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
        logging.error("Ping Bedrock gagal: %s", e)
        return 0

def send_command(cmd: str):
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/command"
    try:
        r = requests.post(url, headers=HEADERS, json={"command": cmd}, timeout=10)
        if r.status_code == 204:
            logging.info("✔️  Perintah terkirim: %s", cmd)
        else:
            logging.error("❌  Kirim perintah gagal. Status: %s", r.status_code)
    except Exception as e:
        logging.error("❌  Error koneksi API: %s", e)

def main():
    while True:
        players = get_online_players()
        if players == 0:
            logging.info("👤 0 pemain online → stop waktu")
            send_command("gamerule doDaylightCycle false")
        else:
            logging.info("🎮 %s pemain online → start waktu", players)
            send_command("gamerule doDaylightCycle true")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    start = time.time()
    print("⏳ Mulai:", datetime.datetime.now().isoformat())
    main()
    print("✅ Selesai:", datetime.datetime.now().isoformat())
    print(f"⏱️ Durasi: {time.time() - start:.2f} detik")
