import pytest

from experiments.implementation_registry import (
    ImplementationRegistry,
)
from experiments.experiment_resolver import (
    ExperimentResolver,
)


class DummyExperiment:
    pass


def create_resolver():
    registry = ImplementationRegistry()

    registry.register(
        "zn_hcl",
        DummyExperiment,
    )

    return ExperimentResolver(registry)


def test_create_returns_new_instance():
    resolver = create_resolver()

    experiment = resolver.create(
        "zn_hcl"
    )

    assert isinstance(
        experiment,
        DummyExperiment,
    )


def test_create_unknown_id_raises_key_error():
    resolver = create_resolver()

    with pytest.raises(KeyError):
        resolver.create(
            "unknown"
        )


def test_create_returns_new_instance_each_time():
    resolver = create_resolver()

    first = resolver.create(
        "zn_hcl"
    )

    second = resolver.create(
        "zn_hcl"
    )

    assert first is not second