import requests
import time
import logging
import os

# Konfigurasi logging agar output muncul di Railway Console
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Isi token API Pterodactyl milikmu di bawah ini
API_KEY = os.getenv("PTERODACTYL_API_KEY", "PASTE_TOKEN_API_KAMU_DI_SINI")

# Ubah ID server kamu di bawah ini (dari Pterodactyl panel)
SERVER_ID = os.getenv("PTERODACTYL_SERVER_ID", "PASTE_ID_SERVER_KAMU_DI_SINI")

# URL endpoint API Pterodactyl
API_URL = os.getenv("PTERODACTYL_API_URL", "https://panel.kagestore.com/api/client")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "Application/vnd.pterodactyl.v1+json",
    "Content-Type": "application/json"
}

def get_players():
    """Ambil data pemain dari API Pterodactyl."""
    try:
        url = f"{API_URL}/servers/{SERVER_ID}/resources"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data["attributes"]["current_state"], data["attributes"]["players"]["count"]
        else:
            logging.error("Gagal mengambil data pemain. Status: %d", response.status_code)
            return None, 0
    except Exception as e:
        logging.error("Terjadi kesalahan saat mengambil data pemain: %s", e)
        return None, 0

def send_command(command):
    """Kirim perintah ke server via API."""
    try:
        url = f"{API_URL}/servers/{SERVER_ID}/command"
        payload = { "command": command }
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 204:
            logging.info("✔️  Berhasil menjalankan perintah: %s", command)
        else:
            logging.error("❌  Gagal mengirim perintah. Status: %d", response.status_code)
    except Exception as e:
        logging.error("❌  Gagal mengirim perintah: %s", e)

def main():
    while True:
        state, player_count = get_players()
        if state != "running":
            logging.info("💤 Server tidak berjalan.")
        elif player_count == 0:
            logging.info("👤 Tidak ada pemain online → menghentikan waktu...")
            send_command("gamerule doDaylightCycle false")
        else:
            logging.info("🧍 Pemain terdeteksi → menyalakan waktu...")
            send_command("gamerule doDaylightCycle true")
        time.sleep(30)

if __name__ == "__main__":
    main()
