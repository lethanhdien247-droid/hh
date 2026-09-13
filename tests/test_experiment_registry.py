import pytest
from experiments.registry import ExperimentRegistry
from experiments.zn_hcl import ZnHClExperiment
from models.experiment_definition import (
    ExperimentDefinition,
)
#===================
from loaders.experiment_data_loader import (
    ExperimentDataLoader,
)
#===========================
def test_registry_load_definition_propagates_loader_error():
    """
    Nếu DataLoader không tìm thấy Experiment,
    Registry phải giữ nguyên lỗi.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    registry = ExperimentRegistry(
        data_loader=loader
    )

    with pytest.raises(
        FileNotFoundError
    ):
        registry.load_definition(
            "does_not_exist"
        )
#==========================
def test_registry_load_definition_requires_loader():
    """
    Không có DataLoader thì không thể load Definition.
    """

    registry = ExperimentRegistry()

    with pytest.raises(
        RuntimeError
    ):
        registry.load_definition(
            "zn_hcl"
        )
#================================
def test_registry_load_definition_from_data_loader():
    """
    Registry phải có thể load Definition
    thông qua DataLoader.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    registry = ExperimentRegistry(
        data_loader=loader
    )

    definition = registry.load_definition(
        "zn_hcl"
    )

    assert isinstance(
        definition,
        ExperimentDefinition,
    )

    assert definition.id == "zn_hcl"

    assert (
        registry.get_definition(
            "zn_hcl"
        )
        is definition
    )

def create_test_definition():
    return ExperimentDefinition(
        id="zn_hcl",
        name="Zn + HCl",
        category="Kim loại + axit",
        description="Kẽm tác dụng với axit clohiđric.",
        equation="Zn + 2HCl → ZnCl₂ + H₂",
        available=True,
    )


def test_registry_get_definition():
    """
    Registry phải trả về ExperimentDefinition
    bằng get_definition().
    """

    definition = create_test_definition()

    registry = ExperimentRegistry(
        definitions=[definition]
    )

    result = registry.get_definition(
        "zn_hcl"
    )

    assert result is definition
    assert isinstance(
        result,
        ExperimentDefinition,
    )


def test_registry_get_unknown_definition():
    """
    Definition không tồn tại phải trả về None.
    """

    registry = ExperimentRegistry()

    assert (
        registry.get_definition(
            "unknown_experiment"
        )
        is None
    )


def test_registry_get_returns_implementation():
    """
    get() vẫn phải trả về Experiment implementation,
    không phải ExperimentDefinition.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_test_definition()
        ]
    )

    experiment = registry.get(
        "zn_hcl"
    )

    assert isinstance(
        experiment,
        ZnHClExperiment,
    )

    assert not isinstance(
        experiment,
        ExperimentDefinition,
    )


def test_registry_register_definition():
    """
    Registry phải cho phép đăng ký Definition.
    """

    registry = ExperimentRegistry()

    definition = create_test_definition()

    registered = (
        registry.register_definition(
            definition
        )
    )

    assert registered is definition

    assert (
        registry.get_definition(
            "zn_hcl"
        )
        is definition
    )

    assert (
        registry.definition_count()
        == 1
    )


def test_registry_reject_invalid_definition():
    """
    Registry không nhận object không phải
    ExperimentDefinition.
    """

    registry = ExperimentRegistry()

    try:
        registry.register_definition(
            {
                "id": "zn_hcl"
            }
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Registry phải từ chối "
            "Definition không hợp lệ."
        )


def test_registry_reject_duplicate_definition():
    """
    Không cho phép hai Definition cùng id.
    """

    definition_1 = (
        create_test_definition()
    )

    definition_2 = (
        ExperimentDefinition(
            id="zn_hcl",
            name="Another Zn + HCl",
            category="Test",
            description="Test",
            equation="A → B",
            available=True,
        )
    )

    registry = ExperimentRegistry(
        definitions=[definition_1]
    )

    try:
        registry.register_definition(
            definition_2
        )
    except ValueError as exc:
        assert (
            "đã được đăng ký"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Registry phải từ chối "
            "Definition trùng id."
        )


def test_registry_get_all_definitions_returns_copy():
    """
    get_all_definitions() phải trả về list mới.
    """

    definition = create_test_definition()

    registry = ExperimentRegistry(
        definitions=[definition]
    )

    definitions = (
        registry.get_all_definitions()
    )

    assert isinstance(
        definitions,
        list,
    )

    assert len(definitions) == 1

    definitions.clear()

    assert (
        registry.definition_count()
        == 1
    )

    assert (
        registry.get_definition(
            "zn_hcl"
        )
        is definition
    )