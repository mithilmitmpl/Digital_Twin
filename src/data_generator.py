import datetime
import random
from typing import List, Dict, Optional

from src.data_model import SensorReading

# Define the sensors on the bridge
# Parameters (mean, std_dev) are for normal operating conditions.
SENSORS: List[Dict] = [
    {'sensor_id': 'ST001', 'location': 'Deck_Midspan', 'measurement_type': 'Strain', 'params': {'mean': 150.0, 'std_dev': 5.0}},
    {'sensor_id': 'ST002', 'location': 'Tower1_Base', 'measurement_type': 'Strain', 'params': {'mean': 50.0, 'std_dev': 2.0}},
    {'sensor_id': 'AC001', 'location': 'Deck_Midspan', 'measurement_type': 'Accelerometer', 'params': {'mean': 0.0, 'std_dev': 0.05}},
    {'sensor_id': 'AC002', 'location': 'Tower1_Top', 'measurement_type': 'Accelerometer', 'params': {'mean': 0.0, 'std_dev': 0.1}},
    {'sensor_id': 'TM001', 'location': 'Asphalt_Surface', 'measurement_type': 'Temperature', 'params': {'mean': 25.0, 'std_dev': 1.5}},
    {'sensor_id': 'DS001', 'location': 'SuspensionCable_A1', 'measurement_type': 'Displacement', 'params': {'mean': 10.0, 'std_dev': 0.5}},
]

class DataGenerator:
    """
    Generates synthetic sensor data for the smart bridge.
    Includes functionality for data quality issues and event simulation.
    """

    def __init__(self, sensor_definitions: List[Dict]):
        """
        Initializes the generator with a list of sensor definitions.
        """
        self.sensors = sensor_definitions

    def _generate_normal_value(self, params: dict) -> float:
        """Generates a single sensor value under normal conditions using a Gaussian distribution."""
        return random.gauss(params['mean'], params['std_dev'])

    def _generate_outlier_value(self, params: dict) -> float:
        """Generates an outlier value, significantly outside the normal range."""
        # Generate a value with a much larger standard deviation
        return random.gauss(params['mean'], params['std_dev'] * 5)

    def _apply_event_effect(self, value: float, sensor_info: dict, event: str) -> float:
        """Modifies a sensor value based on a simulated event."""
        if event == 'OVERLOAD' and sensor_info['measurement_type'] == 'Strain':
            return value * 1.8  # 80% increase in strain
        if event == 'EARTHQUAKE':
            if sensor_info['measurement_type'] == 'Accelerometer':
                return value + random.uniform(-2.0, 2.0)  # Simulate intense shaking
            if sensor_info['measurement_type'] == 'Displacement':
                return value + random.uniform(-15.0, 15.0) # Simulate large displacement
        return value

    def generate(self,
                 timestamp: datetime.datetime,
                 missing_value_prob: float = 0.0,
                 outlier_prob: float = 0.0,
                 event: Optional[str] = None) -> List[SensorReading]:
        """
        Generates a list of sensor readings for a specific timestamp.

        Args:
            timestamp: The timestamp for the readings.
            missing_value_prob: The probability (0-1) of a value being missing.
            outlier_prob: The probability (0-1) of a value being an outlier.
            event: An optional string representing a simulated event (e.g., 'OVERLOAD').
        """
        readings = []
        for sensor_info in self.sensors:
            base_value = self._generate_normal_value(sensor_info['params'])
            final_value: Optional[float] = base_value
            quality_flag = 'GOOD'

            # Apply event effects first, as they are deterministic
            if event:
                final_value = self._apply_event_effect(base_value, sensor_info, event)

            # Then, introduce random quality issues if no major event is active
            if not event:
                if random.random() < outlier_prob:
                    final_value = self._generate_outlier_value(sensor_info['params'])
                    quality_flag = 'OUTLIER'

            if random.random() < missing_value_prob:
                final_value = None
                quality_flag = 'MISSING'

            reading = SensorReading(
                timestamp=timestamp,
                sensor_id=sensor_info['sensor_id'],
                location=sensor_info['location'],
                measurement_type=sensor_info['measurement_type'],
                value=round(final_value, 4) if final_value is not None else None,
                quality_flag=quality_flag
            )
            readings.append(reading)
        return readings
