import asyncio
from datetime import datetime
from app.core.config import settings


class ExampleListener:
    def __init__(self):
        pass

    @staticmethod
    async def start_listener() -> None:
        while True:
            try:
                print(f"Example Datetime: {datetime.now()}")
            except Exception as e:
                print(f"[ERROR] poll_plant_data exception: {e}")

            await asyncio.sleep(settings.EXAMPLE_LISTENER_INTERVAL_SECOND)
