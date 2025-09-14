import argparse
import json
import datetime
import dataclasses
from collections import defaultdict

from src.bridge_model import BRIDGE_MODEL
from src.data_generator import DataGenerator, SENSORS
from src.sensor_mapping import SENSOR_TO_COMPONENT_MAPPING
from src.data_model import SensorReading

def generate_twin_state() -> dict:
    """
    Generates a complete snapshot of the digital twin's state,
    linking sensor readings to their corresponding bridge components.
    """
    # 1. Generate a fresh set of sensor readings
    generator = DataGenerator(SENSORS)
    now = datetime.datetime.utcnow()
    sensor_readings = generator.generate(now)

    # 2. Create a dictionary to hold sensor readings grouped by component ID
    readings_by_component = defaultdict(list)
    for reading in sensor_readings:
        component_id = SENSOR_TO_COMPONENT_MAPPING.get(reading.sensor_id)
        if component_id:
            # We only need a subset of the reading info for the component
            sensor_info = {
                "sensor_id": reading.sensor_id,
                "measurement_type": reading.measurement_type,
                "value": reading.value,
                "quality_flag": reading.quality_flag,
            }
            readings_by_component[component_id].append(sensor_info)

    # 3. Build the final JSON structure
    twin_model = []
    for component in BRIDGE_MODEL:
        component_dict = dataclasses.asdict(component)
        # Add the sensor data to the component
        component_dict["sensors"] = readings_by_component.get(component.component_id, [])
        twin_model.append(component_dict)

    # 4. Assemble the final state object
    twin_state = {
        "timestamp": now.isoformat(),
        "bridge_model": twin_model,
    }

    return twin_state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export the current state of the Smart Bridge Digital Twin to JSON.")
    parser.add_argument("--output-file", type=str, help="Path to JSON file to save the output. If not provided, prints to console.")

    args = parser.parse_args()

    # Generate the state
    state = generate_twin_state()

    # Output the state
    if args.output_file:
        with open(args.output_file, 'w') as f:
            json.dump(state, f, indent=4)
        print(f"Digital twin state exported to {args.output_file}")
    else:
        print(json.dumps(state, indent=4))
