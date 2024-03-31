from dataclasses import dataclass
from typing import TypedDict


@dataclass
class DetectedCar:
    image_url: str


class VehicleSpeed(TypedDict):
    kph: float
    reliability: float
    direction_label: str
    direction: float


class VehicleCoordinates(TypedDict):
    x: float
    y: float
    width: float
    height: float


class DetectedVehicle(TypedDict):
    vehicle_id: int
    vehicle_type: str
    detection_confidence: float
    vehicle_coordinates: VehicleCoordinates
    vehicle_frame_base64: str  # Обрезанный квадратик с машины
    color_info: str
    model_info: str
    speed_info: VehicleSpeed


class TrackingResponse(TypedDict):
    detected_vehicles: list[DetectedVehicle]
    annotated_frame_base64: str
    original_frame_base64: str
