import requests

DEFAULT_BEARER_ID = 9

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
        self.ues[str(ue_id)] = {"transfer": 0, "bearers": {DEFAULT_BEARER_ID}}

    def _resolve_single_ue(self):
        if len(self.ues) != 1:
            raise Exception("error: ue id required")
        return next(iter(self.ues))

    def add_bearer(self, bearer_id, ue_id=None):
        target_ue_id = str(ue_id) if ue_id is not None else self._resolve_single_ue()
        if target_ue_id not in self.ues:
            raise Exception("error: ue not connected")
        self.ues[target_ue_id]["bearers"].add(int(bearer_id))

    def verify_bearer_exists(self, ue_id, bearer_id):
        if str(ue_id) not in self.ues:
            raise Exception("error: ue not connected")
        if int(bearer_id) not in self.ues[str(ue_id)]["bearers"]:
            raise Exception(f"error: bearer {bearer_id} does not exist for ue {ue_id}")

    def remove_bearer(self, bearer_id, ue_id=None):
        target_ue_id = str(ue_id) if ue_id is not None else self._resolve_single_ue()
        if target_ue_id not in self.ues:
            raise Exception("error: ue not connected")
        if int(bearer_id) == DEFAULT_BEARER_ID:
            raise Exception("error: default bearer cannot be removed")
        if int(bearer_id) not in self.ues[target_ue_id]["bearers"]:
            raise Exception(f"error: bearer {bearer_id} does not exist")
        self.ues[target_ue_id]["bearers"].remove(int(bearer_id))

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

    def detach_ue(self, ue_id):
# TC_03 - Pomyślne odłączenie (Detach)
        if str(ue_id) in self.ues: del self.ues[str(ue_id)]
