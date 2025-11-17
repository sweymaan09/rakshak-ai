# Guardian Agent – Loop agent for continuous monitoring
import time
from src.utils.observability import logger

class GuardianAgent:
    def __init__(self):
        self.running = False

    def start(self, steps=5):
        self.running = True
        logs = []

        for i in range(steps):
            if not self.running:
                break
            logs.append(f"tick {i}")
            logger.info(f"[GuardianAgent] tick {i}")
            time.sleep(0.1)
        
        return logs

    def stop(self):
        self.running = False
