import requests import time import logging

Konfigurasi API Pterodactyl

PANEL_URL = "https://dash.kagestore.com" SERVER_ID = "6dcd0d03"  # ID server kamu API_KEY = "q2Pyhlz0JbGEJcO2rLD7sZZrxL1v4AYEfs0pCCZ3"  # API key kamu

Konfigurasi waktu jeda (dalam detik)

DELAY = 60

Setup logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

def get_players(): url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/utilization" headers = { "Authorization": f"Bearer {API_KEY}", "Accept": "application/json", "Content-Type": "application/json" } try: response = requests.get(url, headers=headers) if response.status_code == 200: data = response.json() players = data.get("attributes", {}).get("resources", {}).get("players", 0) return players else: logging.error("Gagal mengambil data pemain. Status: %s", response.status_code) return 0 except Exception as e: logging.error("Terjadi kesalahan saat mengambil data pemain: %s", e) return 0

def send_command(command): url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/command" headers = { "Authorization": f"Bearer {API_KEY}", "Accept": "application/json", "Content-Type": "application/json" } try: response = requests.post(url, headers=headers, json={"command": command}) if response.status_code == 204: logging.info("\u2705  Berhasil menjalankan perintah: %s", command) else: logging.error("\u274C  Gagal menjalankan perintah: %s, Status: %s", command, response.status_code) except Exception as e: logging.error("Terjadi kesalahan saat mengirim perintah: %s", e)

def main(): while True: players = get_players() if players == 0: logging.info("\U0001F464 Tidak ada pemain online → menghentikan waktu...") send_command("gamerule doDaylightCycle false") else: logging.info("\U0001F3AE %s pemain online → menyalakan waktu...", players) send_command("gamerule doDaylightCycle true") time.sleep(DELAY)

if name == "main": main()

