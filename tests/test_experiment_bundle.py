import pytest

from models.experiment_definition import (
    ExperimentDefinition,
)

from experiments.experiment_bundle import (
    ExperimentBundle,
)


class DummyExperiment:
    id = "zn_hcl"


class WrongExperiment:
    id = "fe_hcl"


def create_definition():
    return ExperimentDefinition(
        id="zn_hcl",
        name="Zn + HCl",
        category="Test",
        description="Test experiment",
        equation="Zn + 2HCl → ZnCl2 + H2",
        available=True,
    )


def test_bundle_contains_definition():
    definition = create_definition()
    experiment = DummyExperiment()

    bundle = ExperimentBundle(
        definition,
        experiment,
    )

    assert bundle.definition is definition


def test_bundle_contains_implementation():
    definition = create_definition()
    experiment = DummyExperiment()

    bundle = ExperimentBundle(
        definition,
        experiment,
    )

    assert bundle.experiment is experiment


def test_bundle_id_matches_definition():
    definition = create_definition()
    experiment = DummyExperiment()

    bundle = ExperimentBundle(
        definition,
        experiment,
    )

    assert bundle.id == "zn_hcl"


def test_bundle_rejects_mismatched_ids():
    definition = create_definition()
    experiment = WrongExperiment()

    with pytest.raises(ValueError):
        ExperimentBundle(
            definition,
            experiment,
        )


def test_bundle_rejects_missing_definition():
    experiment = DummyExperiment()

    with pytest.raises(ValueError):
        ExperimentBundle(
            None,
            experiment,
        )


def test_bundle_rejects_missing_implementation():
    definition = create_definition()

    with pytest.raises(ValueError):
        ExperimentBundle(
            definition,
            None,
        )