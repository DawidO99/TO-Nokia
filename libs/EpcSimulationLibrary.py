class EpcSimulationLibrary:
    def __init__(self):
        self.ues = {}

    def reset_simulator(self):
#tc_10 - reset symulatora (czyszczenie srodowiska)
        self.ues.clear()

    def attach_ue(self, ue_id):
#tc_07 - proba podlaczenia juz aktywnego ue (test negatywny)
        if str(ue_id) in self.ues:
            raise Exception(f"error: ue {ue_id} already connected")
        self.ues[str(ue_id)] = {"transfer": 0}

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
        if str(ue_id) in self.ues: del self.ues[str(ue_id)]