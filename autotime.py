import os
import requests
import logging

# Konfigurasi logging
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Konfigurasi server kamu
PTERO_API_KEY = "ptlc_5Zan3yafaZN4HibIZ7hOVaTQ5g7txRB3yg7ocXdwopW"
PTERO_PANEL_URL = "https://dash.kagestore.com"
SERVER_ID = "bdb20976"

HEADERS = {
    "Authorization": f"Bearer {PTERO_API_KEY}",
    "Accept": "Application/vnd.pterodactyl.v1+json",
    "Content-Type": "application/json",
}

def get_players():
    url = f"{PTERO_PANEL_URL}/api/client/servers/{SERVER_ID}/utilization"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data.get("attributes", {}).get("resources", {}).get("players", 0)
    else:
        logging.error("Gagal mengambil data pemain. Status:", response.status_code)
        return 0

def send_command(command):
    url = f"{PTERO_PANEL_URL}/api/client/servers/{SERVER_ID}/command"
    data = {"command": command}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 204:
        logging.info(f"✔️  Berhasil menjalankan perintah: {command}")
    else:
        logging.error(f"❌  Gagal menjalankan perintah: {command}. Status: {response.status_code}")

def main():
    players = get_players()
    if players == 0:
        logging.info("👤 Tidak ada pemain online → menghentikan waktu...")
        send_command("gamerule doDaylightCycle false")
    else:
        logging.info(f"👥 {players} pemain online → menyalakan waktu...")
        send_command("gamerule doDaylightCycle true")

if __name__ == "__main__":
    main()
