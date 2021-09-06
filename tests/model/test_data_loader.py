"""
Test suites for DataLoader
"""
from datetime import timedelta

import pytest

from srca.model.data_loader import DataLoader
from srca.model.data_loader import MemoryDataLoader


@pytest.mark.parametrize(
    ("start", "end", "interval"),
    [
        (100, 280, timedelta(seconds=30)),
        (100, 280, timedelta(seconds=60)),
        (60, 200, timedelta(seconds=60)),
        (60, 280, timedelta(seconds=60)),
        (60, 360, timedelta(seconds=60)),
        (120, 360, timedelta(seconds=60)),
    ],
)
def test_preprocess(start: float, end: float, interval: timedelta):
    """
    Test case for DataLoader.preprocess
    """
    time_series = [
        (100, 1.5),
        (159, 2),
        (221, 3),
        (280, 1),
    ]
    data = DataLoader.preprocess(
        time_series=time_series, start=start, end=end, interval=interval
    )
    assert len(data) == int((end - start) / interval.total_seconds()) + 1
    assert all(isinstance(item, (float, int)) for item in data)


def test_memory_data_loader():
    """
    Test case for MemoryDataLoader
    """
    data = {
        "db": {
            "transaction per second": [
                (100, 1000),
                (159, 1200),
                (221, 1100),
            ],
            "average active sessions": [
                (100, 10),
                (159, 12.5),
                (221, 10.3),
            ],
        },
        "storage": {
            "iops": [
                (99, 2000),
                (159, 5000),
                (219, 4000),
            ],
        },
    }
    data_loader = MemoryDataLoader(data)
    assert set(data_loader.entities) == {"db", "storage"}
    metrics = {entity: set(metrics) for entity, metrics in data_loader.metrics.items()}
    assert metrics == {
        "db": {"transaction per second", "average active sessions"},
        "storage": {
            "iops",
        },
    }
    assert (
        len(
            data_loader.load(
                "db",
                "transaction per second",
                start=60,
                end=300,
                interval=timedelta(seconds=60),
            )
        )
        == 5
    )
