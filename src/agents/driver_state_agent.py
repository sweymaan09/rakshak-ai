# Driver State Agent – combines signals from Vision + OBD
from src.utils.observability import logger

class DriverStateAgent:
    def infer_state(self, vision_obs, obd_obs):
        drowsy = vision_obs["drowsy_score"] > 0.6
        phone = vision_obs["phone_detected"]
        brake_issue = obd_obs.get("brake_flag", 0)

        state = "ALERT"
        if drowsy:
            state = "DROWSY"
        if phone:
            state = "DISTRACTED"
        if brake_issue:
            state = "MECHANICAL_RISK"

        logger.info(f"[DriverStateAgent] State -> {state}")
        return state
