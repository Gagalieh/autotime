#!/usr/bin/env python3
"""
AutoTime Bedrock
────────────────
• Pause waktu (daylight cycle) saat server kosong
• Hidupkan lagi saat ada pemain
Requires: mcstatus, mcrcon
"""

from mcstatus import BedrockServer
from mcrcon import MCRcon

# ── Konfigurasi ───────────────────────────────────────────────
BEDROCK_HOST = "shared14.kagestore.xyz"
BEDROCK_PORT = 19134          # port game Bedrock
RCON_HOST    = "shared14.kagestore.xyz"
RCON_PORT    = 19136          # port RCON (set di server.properties)
RCON_PASS    = "742009gal"
# ──────────────────────────────────────────────────────────────

def get_online_players() -> int:
    """Kembalikan jumlah pemain online; kalau gagal, −1."""
    try:
        status = BedrockServer.lookup(f"{BEDROCK_HOST}:{BEDROCK_PORT}").status()
        return status.players.online
    except Exception as e:
        print(f"[ERR] Gagal ping Bedrock → {e}")
        return -1

def send_rcon(cmd: str) -> None:
    """Kirim perintah ke RCON; cetak error jika gagal."""
    try:
        with MCRcon(RCON_HOST, RCON_PASS, port=RCON_PORT) as rcon:
            rcon.command(cmd)
            print(f"[OK ] RCON sent → {cmd}")
    except Exception as e:
        print(f"[ERR] RCON failed → {e}")

def main():
    online = get_online_players()
    if online == -1:
        return                                  # ping gagal; jangan ubah apa-apa

    print(f"[INFO] Players online = {online}")

    cmd = "gamerule doDaylightCycle true" if online > 0 else \
          "gamerule doDaylightCycle false"
    send_rcon(cmd)

if __name__ == "__main__":
    main()
