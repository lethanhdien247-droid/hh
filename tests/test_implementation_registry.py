import pytest

from experiments.implementation_registry import (
    ImplementationRegistry,
)


class DummyExperiment:
    pass


class AnotherExperiment:
    pass


def test_register_factory():
    registry = ImplementationRegistry()

    registry.register(
        "zn_hcl",
        DummyExperiment,
    )

    assert registry.has("zn_hcl")


def test_get_factory():
    registry = ImplementationRegistry()

    registry.register(
        "zn_hcl",
        DummyExperiment,
    )

    factory = registry.get_factory("zn_hcl")

    assert factory is DummyExperiment


def test_unknown_factory_raises_key_error():
    registry = ImplementationRegistry()

    with pytest.raises(KeyError):
        registry.get_factory("unknown")


def test_duplicate_registration_raises_value_error():
    registry = ImplementationRegistry()

    registry.register(
        "zn_hcl",
        DummyExperiment,
    )

    with pytest.raises(ValueError):
        registry.register(
            "zn_hcl",
            AnotherExperiment,
        )


def test_invalid_factory_raises_type_error():
    registry = ImplementationRegistry()

    with pytest.raises(TypeError):
        registry.register(
            "zn_hcl",
            "not callable",
        )


def test_has_returns_false_for_unknown_id():
    registry = ImplementationRegistry()

    assert registry.has("unknown") is False