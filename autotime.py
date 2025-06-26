from mcstatus import BedrockServer
from mcrcon import MCRcon

# Konfigurasi server
RCON_HOST = "shared14.kagestore.xyz"
RCON_PORT = 19136
RCON_PASSWORD = "742009gal"
BEDROCK_HOST = "shared14.kagestore.xyz"
BEDROCK_PORT = 19134

# Cek jumlah pemain online
server = BedrockServer.lookup(f"{BEDROCK_HOST}:{BEDROCK_PORT}")
status = server.status()
players_online = status.players.online

# Tentukan perintah
if players_online > 0:
    cmd = "gamerule doDaylightCycle true"
else:
    cmd = "gamerule doDaylightCycle false"

# Kirim ke RCON
try:
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        mcr.command(cmd)
        print(f"[INFO] Command sent: {cmd}")
except Exception as e:
    print(f"[ERROR] RCON failed: {e}")