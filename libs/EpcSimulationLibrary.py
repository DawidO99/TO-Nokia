class EpcSimulationLibrary:
    def __init__(self):
        self.ues = {}

    def reset_simulator(self):
#tc_10 - reset symulatora (czyszczenie srodowiska)
        self.ues.clear()

    def attach_ue(self, ue_id):
# TC_01 - Walidacja zakresu ID
        if not (0 <= int(ue_id) <= 100):
            raise Exception(f"error: ue id {ue_id} out of range")

#tc_07 - proba podlaczenia juz aktywnego ue (test negatywny)
        if str(ue_id) in self.ues:
            raise Exception(f"error: ue {ue_id} already connected")

# TC_02 - po attach UE dostaje domyslny bearer 9
        self.ues[str(ue_id)] = {"transfer": 0, "bearers": {9}}

    def start_dl_transfer(self, ue_id, speed, bearer_id=9):
        val = int(''.join(filter(str.isdigit, speed)))

#tc_09 - przekroczenie limitu transferu 100 mbps (test negatywny)
        if "Mbps" in speed and val > 100:
            raise Exception(f"error: speed {speed} exceeds limit")

#tc_05 - rozpoczecie transferu downlink (sukces)
        if str(ue_id) not in self.ues:
            raise Exception("error: ue not connected")
        self.ues[str(ue_id)]["transfer"] = val

    def verify_ue_is_connected(self, ue_id):
        if str(ue_id) not in self.ues: raise Exception("not connected")

    def verify_ue_is_disconnected(self, ue_id):
        if str(ue_id) in self.ues: raise Exception("still connected")

    def verify_dl_transfer(self, ue_id, expected_speed):
        if self.ues[str(ue_id)]["transfer"] == 0: raise Exception("no transfer")

    def add_bearer(self, ue_id, bearer_id):
# TC_04 - dodanie dedykowanego bearera
        ue_key = str(ue_id)
        bearer = int(bearer_id)
        if ue_key not in self.ues:
            raise Exception("error: ue not connected")
        self.ues[ue_key]["bearers"].add(bearer)

    def verify_bearer_exists(self, ue_id, bearer_id):
        ue_key = str(ue_id)
        bearer = int(bearer_id)
        if ue_key not in self.ues:
            raise Exception("error: ue not connected")
        if bearer not in self.ues[ue_key]["bearers"]:
            raise Exception(f"error: bearer {bearer_id} not assigned to ue {ue_id}")

    def detach_ue(self, ue_id):
# TC_03 - Pomyślne odłączenie (Detach)
        if str(ue_id) in self.ues: del self.ues[str(ue_id)]

# TC_08 - Blokada usunięcia domyślnego bearera (ID 9)
    def remove_bearer(self, ue_id, bearer_id):
        ue_key = str(ue_id)
        bearer = int(bearer_id)

        if ue_key not in self.ues:
            raise Exception("error: ue not connected")

        if bearer == 9:
            raise Exception("error: cannot remove default bearer")

        self.ues[ue_key]["bearers"].remove(bearer)