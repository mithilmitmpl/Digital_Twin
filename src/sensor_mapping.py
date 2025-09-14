from typing import Dict, Optional

# This dictionary maps each sensor's unique ID to the ID of the bridge component it is attached to.
# This creates the link between the sensor data (Phase 1) and the 3D model (Phase 2).
SENSOR_TO_COMPONENT_MAPPING: Dict[str, str] = {
    # Strain Gauges
    'ST001': 'DECK-MAIN',  # Original Location hint: Deck_Midspan
    'ST002': 'TWR-N',      # Original Location hint: Tower1_Base (maps to North Tower)

    # Accelerometers
    'AC001': 'DECK-MAIN',  # Original Location hint: Deck_Midspan
    'AC002': 'TWR-N',      # Original Location hint: Tower1_Top

    # Temperature Sensor
    'TM001': 'DECK-MAIN',  # Original Location hint: Asphalt_Surface (on the main deck)

    # Displacement Meter
    'DS001': 'CBL-M-E',    # Original Location hint: SuspensionCable_A1 (maps to East Main Cable)
}

def get_component_id_for_sensor(sensor_id: str) -> Optional[str]:
    """
    Given a sensor ID, returns the corresponding component ID it is mapped to.
    """
    return SENSOR_TO_COMPONENT_MAPPING.get(sensor_id)
