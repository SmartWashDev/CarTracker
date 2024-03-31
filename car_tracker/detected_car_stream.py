import json
from dataclasses import asdict

import nats

from car_tracker.structs import DetectedCar


class DetectedCarNatsStream:
    def __init__(
        self,
        nats_server: str = 'nats://localhost:4222',
        stream_name: str = 'detected_cars',
    ):
        self.stream_name = stream_name
        self.nats_server = nats_server

        self.nc = None

    async def connect(self):
        self.nc = await nats.connect(self.nats_server)

    async def close(self):
        await self.nc.close()

    async def publish(self, item: DetectedCar):
        if not self.nc:
            await self.connect()

        await self.nc.publish(self.stream_name, json.dumps(asdict(item)).encode())
