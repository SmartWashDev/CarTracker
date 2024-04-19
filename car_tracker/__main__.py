from car_tracker.application import VideoCarTracker
from car_tracker.settings import settings

VideoCarTracker(settings.VIDEO_SOURCE).run()
