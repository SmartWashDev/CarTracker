import asyncio
import base64
import io
from datetime import datetime

from minio import Minio
from car_tracker.settings import settings

from car_tracker.detected_car_stream import DetectedCarNatsStream
from car_tracker.structs import DetectedCar, TrackingResponse


class TrackerCallback:
    """
    Сохраняет картинку в минио с3 и отправляет ссылку на нее в натс.
    Отправляет только уникальные автомобили.
    """

    vehicles_labels = ('car', 'track', 'bus', 'motorcycle')

    def __init__(self):
        self._used_vehicles_ids = set()
        self._minio = Minio(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._bucket_name = settings.MINIO_BUCKET_NAME

        self._event_loop = asyncio.get_event_loop()

    def __call__(self, results: TrackingResponse):
        return self.callback(results)

    def callback(self, results: TrackingResponse):
        for vehicle in results['detected_vehicles']:
            # Если это не тс, то скип
            if vehicle['vehicle_type'] not in self.vehicles_labels:
                continue

            # Если тс с таким айди уже сохранялось,то скип
            vehicle_id = vehicle['vehicle_id']
            if vehicle_id in self._used_vehicles_ids:
                continue

            # Сохраняем фото ТС в минио и получаем урл
            vehicle_image = vehicle['vehicle_frame_base64']
            vehicle_image_url = self.save_to_minio_and_get_url(vehicle_id, vehicle_image)

            # Отправляем урл фото в натс
            self.add_image_to_nats(vehicle_image_url)

            # Сохраняем айди авто, чтобы не отправить повторно
            # айди сбрасываются каждую сессию
            self._used_vehicles_ids.add(vehicle_id)

    def save_to_minio_and_get_url(self, vehicle_id: int, vehicle_image: str):
        file_name = f'{datetime.now()}detected_car_{vehicle_id}.jpg'
        self._minio.put_object(
            self._bucket_name,
            file_name,
            io.BytesIO(base64.b64decode(vehicle_image)),
            length=len(base64.b64decode(vehicle_image)),
        )
        return self._minio.get_presigned_url('GET', self._bucket_name, file_name)

    def add_image_to_nats(self, image_url: str):
        detected_car = DetectedCar(image_url=image_url)
        publish_coro = DetectedCarNatsStream().publish(detected_car)
        self._event_loop.run_until_complete(publish_coro)
