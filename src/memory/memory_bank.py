# src/memory/memory_bank.py
import json, time, os
class MemoryBank:
    def __init__(self, path='data/memory.json'):
        self.path = path
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    self.store = json.load(f)
            except:
                self.store = {'hotspots': [], 'trips': []}
        else:
            self.store = {'hotspots': [], 'trips': []}
    def add_hotspot(self, geo, score):
        self.store['hotspots'].append({'geo':geo,'score':score,'ts':time.time()})
        self._flush()
    def add_trip_summary(self, summary):
        self.store['trips'].append(summary)
        self._flush()
    def _flush(self):
        with open(self.path,'w') as f:
            json.dump(self.store, f, indent=2)
