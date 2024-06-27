import unittest
from datetime import datetime
from measurement_sampler import Measurement, MeasurementSampler, MeasType

class TestMeasurementSampler(unittest.TestCase):

    def setUp(self):
        self.measurements = [
            Measurement(datetime.fromisoformat("2017-01-03T10:04:45"), MeasType.TEMP, 35.79),
            Measurement(datetime.fromisoformat("2017-01-03T10:01:18"), MeasType.SPO2, 98.78),
            Measurement(datetime.fromisoformat("2017-01-03T10:09:07"), MeasType.TEMP, 35.01),
            Measurement(datetime.fromisoformat("2017-01-03T10:03:34"), MeasType.SPO2, 96.49),
            Measurement(datetime.fromisoformat("2017-01-03T10:02:01"), MeasType.TEMP, 35.82),
            Measurement(datetime.fromisoformat("2017-01-03T10:05:00"), MeasType.SPO2, 97.17),
            Measurement(datetime.fromisoformat("2017-01-03T10:05:01"), MeasType.SPO2, 95.08),
            Measurement(datetime.fromisoformat("2017-01-03T10:06:45"), MeasType.HR, 70),
            Measurement(datetime.fromisoformat("2017-01-03T10:07:15"), MeasType.HR, 75),
            Measurement(datetime.fromisoformat("2017-01-03T10:08:30"), MeasType.HR, 72),
            Measurement(datetime.fromisoformat("2017-01-03T10:09:45"), MeasType.HR, 74),
            Measurement(datetime.fromisoformat("2017-01-03T10:10:00"), MeasType.TEMP, 34.95),
            Measurement(datetime.fromisoformat("2017-01-03T10:11:45"), MeasType.SPO2, 99.01),
            Measurement(datetime.fromisoformat("2017-01-03T10:12:30"), MeasType.TEMP, 36.02),
            Measurement(datetime.fromisoformat("2017-01-03T10:14:45"), MeasType.HR, 71),
            Measurement(datetime.fromisoformat("2017-01-03T10:15:00"), MeasType.TEMP, 35.47),
            Measurement(datetime.fromisoformat("2017-01-03T10:16:15"), MeasType.SPO2, 96.55),
            Measurement(datetime.fromisoformat("2017-01-03T10:18:30"), MeasType.HR, 73),
            Measurement(datetime.fromisoformat("2017-01-03T10:19:45"), MeasType.TEMP, 35.12),
            Measurement(datetime.fromisoformat("2017-01-03T10:20:00"), MeasType.SPO2, 97.12),
            Measurement(datetime.fromisoformat("2017-01-03T10:21:15"), MeasType.HR, 76),
            Measurement(datetime.fromisoformat("2017-01-03T10:23:30"), MeasType.TEMP, 35.68),
            Measurement(datetime.fromisoformat("2017-01-03T10:25:45"), MeasType.SPO2, 95.78),
            Measurement(datetime.fromisoformat("2017-01-03T10:27:00"), MeasType.HR, 78),
            Measurement(datetime.fromisoformat("2017-01-03T10:28:30"), MeasType.TEMP, 35.92),
            Measurement(datetime.fromisoformat("2017-01-03T10:30:00"), MeasType.SPO2, 98.22),
        ]
        self.start_of_sampling = datetime.fromisoformat("2017-01-03T10:00:00")

    def test_group_by_type(self):
        grouped = MeasurementSampler.group_by_type(self.measurements)
        self.assertEqual(len(grouped[MeasType.SPO2]), 9)
        self.assertEqual(len(grouped[MeasType.HR]), 8)
        self.assertEqual(len(grouped[MeasType.TEMP]), 9)

    def test_get_interval_start(self):
        dt = datetime.fromisoformat("2017-01-03T10:12:34")
        interval_start = MeasurementSampler.get_interval_start(dt)
        self.assertEqual(interval_start, datetime.fromisoformat("2017-01-03T10:10:00"))

    def test_sample_intervals(self):
        samples = MeasurementSampler.sample_intervals([
            Measurement(datetime.fromisoformat("2017-01-03T10:04:45"), MeasType.TEMP, 35.79),
            Measurement(datetime.fromisoformat("2017-01-03T10:09:07"), MeasType.TEMP, 35.01),
            Measurement(datetime.fromisoformat("2017-01-03T10:02:01"), MeasType.TEMP, 35.82),
            Measurement(datetime.fromisoformat("2017-01-03T10:10:00"), MeasType.TEMP, 34.95),
            Measurement(datetime.fromisoformat("2017-01-03T10:12:30"), MeasType.TEMP, 36.02),
            Measurement(datetime.fromisoformat("2017-01-03T10:15:00"), MeasType.TEMP, 35.47),
            Measurement(datetime.fromisoformat("2017-01-03T10:19:45"), MeasType.TEMP, 35.12),
            Measurement(datetime.fromisoformat("2017-01-03T10:23:30"), MeasType.TEMP, 35.68),
            Measurement(datetime.fromisoformat("2017-01-03T10:28:30"), MeasType.TEMP, 35.92),
        ])
        expected_times = [
            "2017-01-03T10:05:00",
            "2017-01-03T10:10:00",
            "2017-01-03T10:15:00",
            "2017-01-03T10:20:00",
            "2017-01-03T10:25:00",
            "2017-01-03T10:30:00"
        ]
        actual_times = [m.measurement_time.isoformat() for m in samples]
        self.assertEqual(expected_times, actual_times)

    def test_sample_measurements(self):
        sampled = MeasurementSampler.sample_measurements(self.start_of_sampling, self.measurements)

        self.assertIn(MeasType.SPO2, sampled)
        self.assertIn(MeasType.HR, sampled)
        self.assertIn(MeasType.TEMP, sampled)
        
        self.assertEqual(len(sampled[MeasType.SPO2]), 5)  # Updated expected count
        self.assertEqual(len(sampled[MeasType.HR]), 5)
        self.assertEqual(len(sampled[MeasType.TEMP]), 6)

        expected_spo2_times = [
            "2017-01-03T10:05:00",
            "2017-01-03T10:10:00",
            "2017-01-03T10:15:00",
            "2017-01-03T10:20:00",
            "2017-01-03T10:30:00"
        ]
        actual_spo2_times = [m.measurement_time.isoformat() for m in sampled[MeasType.SPO2]]
        self.assertEqual(expected_spo2_times, actual_spo2_times)

        expected_hr_times = [
            "2017-01-03T10:10:00",
            "2017-01-03T10:15:00",
            "2017-01-03T10:20:00",
            "2017-01-03T10:25:00",
            "2017-01-03T10:30:00"
        ]
        actual_hr_times = [m.measurement_time.isoformat() for m in sampled[MeasType.HR]]
        self.assertEqual(expected_hr_times, actual_hr_times)

        expected_temp_times = [
            "2017-01-03T10:05:00",
            "2017-01-03T10:10:00",
            "2017-01-03T10:15:00",
            "2017-01-03T10:20:00",
            "2017-01-03T10:25:00",
            "2017-01-03T10:30:00"
        ]
        actual_temp_times = [m.measurement_time.isoformat() for m in sampled[MeasType.TEMP]]
        self.assertEqual(expected_temp_times, actual_temp_times)

if __name__ == '__main__':
    unittest.main()
