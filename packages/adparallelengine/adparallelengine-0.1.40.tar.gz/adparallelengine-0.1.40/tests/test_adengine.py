import os
import pytest


@pytest.mark.parametrize(
    "gather",
    (True, False),
)
@pytest.mark.parametrize(
    "batched",
    (True, False),
)
@pytest.mark.parametrize(
    "share",
    (True, False),
)
@pytest.mark.parametrize(
    "generator",
    (True, False),
)
@pytest.mark.parametrize(
    "max_cpu",
    ("None", 1),
)
def test_serial(gather, batched, share, generator, max_cpu):
    start("serial", gather, batched, share, generator, max_cpu)


@pytest.mark.parametrize(
    "gather",
    (True, False),
)
@pytest.mark.parametrize(
    "batched",
    (True, False),
)
@pytest.mark.parametrize(
    "share",
    (True, False),
)
@pytest.mark.parametrize(
    "generator",
    (True, False),
)
@pytest.mark.parametrize(
    "max_cpu",
    ("None", 1),
)
def test_multiproc(gather, batched, share, generator, max_cpu):
    start("multiproc", gather, batched, share, generator, max_cpu)


@pytest.mark.parametrize(
    "gather",
    (True, False),
)
@pytest.mark.parametrize(
    "batched",
    (True, False),
)
@pytest.mark.parametrize(
    "share",
    (True, False),
)
@pytest.mark.parametrize(
    "generator",
    (True, False),
)
@pytest.mark.parametrize(
    "max_cpu",
    ("None", 1),
)
def test_dask(gather, batched, share, generator, max_cpu):
    start("dask", gather, batched, share, generator, max_cpu)


def start(which, gather, batched, share, generator, max_cpu):
    assert os.system(
        f"PYTHONPATH=./ python tests/main.py {which} {gather} {batched} {share} {generator} {max_cpu}"
    ) == 0
