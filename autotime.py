#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pause / resume daylight cycle otomatis
• Ping jumlah pemain via mcstatus
• Kirim perintah lewat API Pterodactyl
"""

import os
import time
import logging
import requests
from mcstatus import BedrockServer

# ─── ENV (bisa diedit manual atau lewat Variables Railway) ────────────────────
BEDROCK_HOST = os.getenv("BEDROCK_HOST", "shared14.kagestore.xyz")
BEDROCK_PORT = int(os.getenv("BEDROCK_PORT", 19134))

PANEL_API_URL = os.getenv("PTERODACTYL_API_URL", "https://dash.kagestore.com/api/client")
SERVER_ID     = os.getenv("PTERODACTYL_SERVER_ID", "bdb20976")
API_KEY       = os.getenv("PTERODACTYL_API_KEY", "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))   # detik
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "Application/json",
    "Content-Type": "application/json"
}

def get_online_players() -> int:
    """Ping Bedrock server → kembalikan jumlah pemain online (atau -1 kalau gagal)."""
    try:
        status = BedrockServer.lookup(f"{BEDROCK_HOST}:{BEDROCK_PORT}").status()
        return status.players.online
    except Exception as e:
        logging.error("Gagal ping Bedrock: %s", e)
        return -1

def send_command(cmd: str) -> None:
    """Kirim perintah ke server via API Pterodactyl."""
    url = f"{PANEL_API_URL}/servers/{SERVER_ID}/command"
    try:
        r = requests.post(url, headers=HEADERS, json={"command": cmd}, timeout=10)
        if r.status_code == 204:
            logging.info("✔️ Perintah terkirim: %s", cmd)
        else:
            logging.error("❌ Gagal kirim perintah (%s): %s", r.status_code, cmd)
    except requests.RequestException as e:
        logging.error("❌ Error koneksi API: %s", e)

def main():
    while True:
        online = get_online_players()
        if online == -1:
            logging.info("💤 Server tidak merespons; coba lagi %s detik…", CHECK_INTERVAL)
        elif online == 0:
            logging.info("👤 0 pemain online → hentikan waktu")
            send_command("gamerule doDaylightCycle false")
        else:
            logging.info("🎮 %s pemain online → nyalakan waktu", online)
            send_command("gamerule doDaylightCycle true")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
