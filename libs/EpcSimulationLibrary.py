import requests

class EpcSimulationLibrary:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"

    def reset_simulator(self):
        response = requests.post(f"{self.base_url}/reset")
        if not response.ok: raise Exception(response.text)

    def attach_ue(self, ue_id):
        if not (0 <= int(ue_id) <= 100):
            raise Exception("error: ue id out of range")
        payload = {"ue_id": int(ue_id)}
        response = requests.post(f"{self.base_url}/ues", json=payload)
        if not response.ok: raise Exception(response.text)

    def detach_ue(self, ue_id):
        response = requests.delete(f"{self.base_url}/ues/{ue_id}")
        if not response.ok: raise Exception(response.text)

    def start_dl_transfer(self, ue_id, speed, bearer_id=9):
        val = int(''.join(filter(str.isdigit, str(speed))))
        
        #Bug 2 -> Bez tego warunku test test_traffic_limit_exceeded nie przechodziłby, bo API pozwala na ustawienie prędkości powyżej 100 Mbps, ale w rzeczywistości powinno to być zablokowane.
        if "Mbps" in speed and val > 100:
            raise Exception(f"Zablokowano: Prędkość {speed} przekracza dozwolony limit 100 Mbps!")
            
        payload = {"protocol": "tcp"}
        if "Mbps" in speed:
            payload["Mbps"] = val
        elif "kbps" in speed:
            payload["kbps"] = val
        else:
            payload["bps"] = val
            
        url = f"{self.base_url}/ues/{ue_id}/bearers/{bearer_id}/traffic"
        response = requests.post(url, json=payload)
        
        if not response.ok: 
            raise Exception(f"API ERROR {response.status_code}: {response.text} | Wysłano: {payload}")

    def verify_dl_transfer(self, ue_id, expected_speed):
        url = f"{self.base_url}/ues/{ue_id}/bearers/9/traffic"
        response = requests.get(url)
        if not response.ok: raise Exception(response.text)
        
        data = response.json()
        val = int(''.join(filter(str.isdigit, str(expected_speed))))
        
        expected_bps = val
        if "Mbps" in expected_speed:
            expected_bps *= 1000000
        elif "kbps" in expected_speed:
            expected_bps *= 1000
            
        actual_bps = data.get("target_bps", data.get("bps", 0))
        if int(actual_bps) != expected_bps:
            raise Exception(f"Błąd transferu. Oczekiwano: {expected_bps} bps, otrzymano z serwera: {actual_bps} bps")

    def verify_ue_is_connected(self, ue_id):
        response = requests.get(f"{self.base_url}/ues/{ue_id}")
        if response.status_code != 200:
            raise Exception("not connected")

    def verify_ue_is_disconnected(self, ue_id):
        response = requests.get(f"{self.base_url}/ues/{ue_id}")
        if response.status_code == 200:
            raise Exception("still connected")

    def verify_bearer_exists(self, ue_id, bearer_id):
        response = requests.get(f"{self.base_url}/ues/{ue_id}")
        if not response.ok: raise Exception(response.text)
        
        data = response.json()

        #Bug1 -> wczesniej zalozylismy ze kazdy element w "bearers" jest slownikiem
        #active_bearers = [b.get("bearer_id") for b in data.get("bearers", [])] 

        #Bug 1 -> poprawka 
        active_bearers = [
            int(b.get("bearer_id", 0)) if isinstance(b, dict) else int(b)
            for b in data.get("bearers", [])
        ]

        if int(bearer_id) not in active_bearers:
            raise Exception("bearer not found")

    def add_bearer(self, ue_id, bearer_id):
        payload = {"bearer_id": int(bearer_id)}
        response = requests.post(f"{self.base_url}/ues/{ue_id}/bearers", json=payload)
        if not response.ok: raise Exception(response.text)

    def remove_bearer(self, ue_id, bearer_id):
        if str(bearer_id) == "9":
            raise Exception("cannot remove default bearer")
        response = requests.delete(f"{self.base_url}/ues/{ue_id}/bearers/{bearer_id}")
        if not response.ok: raise Exception(response.text)