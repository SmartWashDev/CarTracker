from collections.abc import Callable

from car_tracker.callback import TrackerCallback
from vehicle_detection_tracker import VehicleDetectionTracker


class VideoCarTracker:
    def __init__(self, video_source: str, callback: Callable = TrackerCallback()):
        self._video_source = video_source
        self._callback = callback

    def run(self):
        vehicle_tracker = VehicleDetectionTracker()
        vehicle_tracker.process_video(self._video_source, self._callback)
