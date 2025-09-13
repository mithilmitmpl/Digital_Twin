import argparse
import csv
import datetime
import sys
import time
import dataclasses
from typing import Optional

from src.data_generator import DataGenerator, SENSORS
from src.data_model import SensorReading

def run_simulation(duration: int, interval: float, output_file: Optional[str], missing_prob: float, outlier_prob: float, event: Optional[str]):
    """
    Runs the real-time data generation simulation.

    Args:
        duration: The total time to run the simulation, in seconds.
        interval: The time to wait between generating data points, in seconds.
        output_file: Optional path to a CSV file to save the generated data.
        missing_prob: The probability (0-1) of a value being missing.
        outlier_prob: The probability (0-1) of a value being an outlier.
        event: An optional string representing a simulated event (e.g., 'OVERLOAD').
    """
    print("Starting bridge sensor simulation...")
    print(f"Running for {duration} seconds with a {interval} second interval.")

    generator = DataGenerator(SENSORS)
    start_time = time.time()

    csv_writer = None
    file_handle = None

    if output_file:
        try:
            file_handle = open(output_file, 'w', newline='')
            csv_writer = csv.writer(file_handle)
            header = [field.name for field in dataclasses.fields(SensorReading)]
            csv_writer.writerow(header)
        except IOError as e:
            print(f"Error: Could not write to output file {output_file}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        end_time = start_time + duration
        while time.time() < end_time:
            now_utc = datetime.datetime.utcnow()

            readings = generator.generate(
                timestamp=now_utc,
                missing_value_prob=missing_prob,
                outlier_prob=outlier_prob,
                event=event  # The event persists for the whole duration if specified
            )

            print(f"--- {now_utc.isoformat()} ---")
            for reading in readings:
                print(reading)
                if csv_writer:
                    # Convert dataclass to a list for the CSV writer
                    csv_writer.writerow(dataclasses.astuple(reading))

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        if file_handle:
            file_handle.close()
            print(f"\nData saved to {output_file}")
        print("Simulation finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Smart Bridge Digital Twin data simulation.")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the simulation in seconds. (Default: 10)")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval between data points in seconds. (Default: 1.0)")
    parser.add_argument("--output-file", type=str, default=None, help="Path to CSV file to save the output. (e.g., data/simulation_output.csv)")
    parser.add_argument("--missing-prob", type=float, default=0.01, help="Probability of missing values (0-1). (Default: 0.01)")
    parser.add_argument("--outlier-prob", type=float, default=0.01, help="Probability of outlier values (0-1). (Default: 0.01)")
    parser.add_argument("--event", type=str, default=None, choices=['OVERLOAD', 'EARTHQUAKE'], help="Simulate a specific event for the entire duration.")

    args = parser.parse_args()

    run_simulation(
        duration=args.duration,
        interval=args.interval,
        output_file=args.output_file,
        missing_prob=args.missing_prob,
        outlier_prob=args.outlier_prob,
        event=args.event
    )
