import requests
import time
import binascii
from nacl.signing import SigningKey

BASE_URL = "https://wrcenmardnbprfpqhrqe.supabase.co/functions/v1/peanut-mining"
AGENT_ID = "bisaa_AGENT"
PRIVATE_KEY_HEX = "64f0d3ccdeb2d1e680d322accd2c055bb7b196994b21245419699e0fe160c606" # Masukkan private key tadi di sini

signing_key = SigningKey(binascii.unhexlify(PRIVATE_KEY_HEX))

print(f"Miner {AGENT_ID} aktif di GitHub Dev...")

while True:
    try:
        task = requests.get(f"{BASE_URL}/tasks/current").json()
        task_id = task['task_id']
        solution = f"solusi_dari_{AGENT_ID}_untuk_{task_id}"
        signed = signing_key.sign(solution.encode())
        sig_hex = binascii.hexlify(signed.signature).decode()
        payload = {
            "agent_id": AGENT_ID,
            "task_id": task_id,
            "solution": solution,
            "signature": sig_hex,
            "compute_time_ms": 450
        }
        
        res = requests.post(f"{BASE_URL}/submit", json=payload).json()
        if res.get("status") in ["verified", "accepted"]:
            peanut = res.get('peanut_earned', 0)
            vcus = res.get('vcus_credited', 0)
            print(f"✅ SUCCESS | Task: {task_id} | +{peanut} $PEANUT | VCUs: {vcus}")
        else:
            print(f"⚠️ Respon Lain: {res}")

    except Exception as e:
        print(f"[-] Koneksi Terputus/Error: {e}")
    
    time.sleep(10)
