# Vision Agent – Mocked Gemini Vision + simple analysis
from src.tools.camera_tool import CameraTool
from src.utils.observability import logger

class VisionAgent:
    def __init__(self):
        self.camera = CameraTool()

    def analyze_frame(self, frame_path):
        """
        Mocked vision analysis – no API key needed.
        """
        result = {
            "drowsy_score": 0.3,
            "phone_detected": False,
            "lane_departure": False,
            "nearby_vehicle": True
        }
        logger.info(f"[VisionAgent] Frame analyzed -> {result}")
        return result
