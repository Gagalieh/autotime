#!/usr/bin/env python3
# autotime.py  –  versi dengan pengukur durasi

import requests
import time
import logging
import datetime

# ──────────────── Konfigurasi ────────────────
PANEL_URL = "https://dash.kagestore.com"
SERVER_ID = "bdb20976"
API_KEY   = "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW"
DELAY     = 60                    # detik
# ─────────────────────────────────────────────

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

def get_players():
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/resources"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data["attributes"]["players"]
        else:
            logging.error("Gagal ambil data pemain. Status: %s", r.status_code)
            return 0
    except Exception as e:
        logging.error("Kesalahan ambil pemain: %s", e)
        return 0

def send_command(cmd: str):
    url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/command"
    try:
        r = requests.post(url, headers=HEADERS, json={"command": cmd}, timeout=10)
        if r.status_code == 204:
            logging.info("✔️  Perintah terkirim: %s", cmd)
        else:
            logging.error("❌  Gagal kirim perintah. Status: %s", r.status_code)
    except Exception as e:
        logging.error("❌  Error kirim perintah: %s", e)

def main():
    players = get_players()
    if players == 0:
        logging.info("👤 0 pemain online → waktu dihentikan")
        send_command("gamerule doDaylightCycle false")
    else:
        logging.info("🎮 %s pemain online → waktu berjalan", players)
        send_command("gamerule doDaylightCycle true")

# ───────  jalankan & ukur durasinya  ────────
if __name__ == "__main__":
    start = time.time()
    print("⏳ Mulai:", datetime.datetime.now().isoformat())

    main()                     # menjalankan logika utama

    akhir = time.time()
    durasi = akhir - start
    print("✅ Selesai:", datetime.datetime.now().isoformat())
    print(f"⏱️ Durasi eksekusi: {durasi:.2f} detik")
