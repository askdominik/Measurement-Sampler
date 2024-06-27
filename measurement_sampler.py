import collections
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List


class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3


@dataclass
class Measurement:
    measurement_time: datetime
    measurement_type: MeasType
    value: float


class MeasurementSampler:
    @staticmethod
    def group_by_type(
        measurements: List[Measurement],
    ) -> Dict[MeasType, List[Measurement]]:
        
        grouped = collections.defaultdict(list)
        for measurement in measurements:
            grouped[measurement.measurement_type].append(measurement)
        return grouped

    @staticmethod
    def get_interval_start(time: datetime) -> datetime:
        return time.replace(second=0, microsecond=0, minute=(time.minute // 5) * 5)

    @staticmethod
    def sample_intervals(measurements: List[Measurement]) -> List[Measurement]:
        interval_data = collections.defaultdict(list)
        for measurement in measurements:
            interval_start = MeasurementSampler.get_interval_start(
                measurement.measurement_time
            )
            if measurement.measurement_time == interval_start:
                interval_data[interval_start].append(measurement)
            else:
                interval_data[interval_start + timedelta(minutes=5)].append(measurement)

        sampled_measurements = []
        for interval_start, interval_measurements in interval_data.items():
            last_measurement = max(
                interval_measurements, key=lambda m: m.measurement_time
            )
            sampled_measurements.append(
                Measurement(
                    measurement_time=interval_start,
                    measurement_type=last_measurement.measurement_type,
                    value=last_measurement.value,
                )
            )
        return sampled_measurements

    @staticmethod
    def sample_measurements(
        start_of_sampling: datetime, unsampled_measurements: List[Measurement]
    ) -> Dict[MeasType, List[Measurement]]:
        grouped_measurements = MeasurementSampler.group_by_type(unsampled_measurements)

        result = collections.defaultdict(list)
        for meas_type, measurements in grouped_measurements.items():
            measurements.sort(key=lambda m: m.measurement_time)
            sampled = MeasurementSampler.sample_intervals(measurements)
            result[meas_type] = sampled

        return result


if __name__ == "__main__":
    unsampled_measurements = [
        Measurement(
            datetime.fromisoformat("2017-01-03T10:04:45"), MeasType.TEMP, 35.79
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:01:18"), MeasType.SPO2, 98.78
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:09:07"), MeasType.TEMP, 35.01
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:03:34"), MeasType.SPO2, 96.49
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:02:01"), MeasType.TEMP, 35.82
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:05:00"), MeasType.SPO2, 97.17
        ),
        Measurement(
            datetime.fromisoformat("2017-01-03T10:05:01"), MeasType.SPO2, 95.08
        ),
    ]

    start_of_sampling = datetime.fromisoformat("2017-01-03T10:00:00")

    sampled_measurements = MeasurementSampler.sample_measurements(
        start_of_sampling, unsampled_measurements
    )

    for meas_type, measurements in sampled_measurements.items():
        print(f"Measurement type: {meas_type.name}")
        for m in measurements:
            print(
                f"{{{m.measurement_time.isoformat()}, {m.measurement_type.name}, {m.value}}}"
            )
