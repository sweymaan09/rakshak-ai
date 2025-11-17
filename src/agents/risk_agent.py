# Risk Agent – Simple rule-based risk score
from src.utils.observability import logger

class RiskAgent:
    def compute_risk(self, vision_obs, driver_state, weather="rain"):
        score = 20

        if driver_state != "ALERT":
            score += 40
        if vision_obs["nearby_vehicle"]:
            score += 20
        if weather == "rain":
            score += 20

        logger.info(f"[RiskAgent] Risk Score -> {score}")
        return score
