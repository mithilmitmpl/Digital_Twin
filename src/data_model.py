import dataclasses
import datetime

@dataclasses.dataclass
class SensorReading:
    """
    Represents a single sensor reading from the bridge.
    """
    timestamp: datetime.datetime
    sensor_id: str
    location: str
    measurement_type: str
    value: float
    quality_flag: str
