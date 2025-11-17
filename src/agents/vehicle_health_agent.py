# Vehicle Health Agent – Reads simulated OBD signals
from src.utils.observability import logger

class VehicleHealthAgent:
    def analyze(self, obd):
        issues = []
        if obd.get("tire", 32) < 27:
            issues.append("LOW_TIRE_PRESSURE")
        if obd.get("brake_flag", 0) == 1:
            issues.append("BRAKE_WARNING")

        logger.info(f"[VehicleHealthAgent] Issues -> {issues}")
        return issues
