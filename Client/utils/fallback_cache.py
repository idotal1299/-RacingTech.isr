import os
import json

class UnsentLapManager:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.buffer = self.load()

    def load(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def add(self, lap_data):
        self.buffer.append(lap_data)
        self.save()

    def save(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.buffer, f)

    def flush(self, sender):
        success = []
        for lap in self.buffer:
            if sender.send(lap):
                success.append(lap)
        self.buffer = [lap for lap in self.buffer if lap not in success]
        self.save()
