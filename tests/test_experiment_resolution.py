import pytest

from models.experiment_definition import ExperimentDefinition
from experiments.registry import ExperimentRegistry


class DummyExperiment:
    """
    Implementation giả dùng để kiểm tra
    Resolution Architecture.

    Không chứa logic hóa học.
    """

    id = "zn_hcl"

    def __init__(self):
        self.created = True


class AnotherDummyExperiment:
    """
    Implementation giả thứ hai để kiểm tra
    duplicate mapping và lifecycle.
    """

    id = "another"


def create_definition():
    return ExperimentDefinition(
        id="zn_hcl",
        name="Zn + HCl",
        category="Test",
        description="Test experiment",
        equation="Zn + 2HCl → ZnCl2 + H2",
        available=True,
    )


# ============================================================
# 1. IMPLEMENTATION MAPPING
# ============================================================

def test_implementation_mapping_register_factory():
    """
    Registry phải cho phép đăng ký factory
    cho một experiment_id.
    """

    registry = ExperimentRegistry()

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    assert registry.has_implementation(
        "zn_hcl"
    )


def test_implementation_mapping_get_factory():
    """
    Registry phải trả lại đúng factory
    đã đăng ký.
    """

    registry = ExperimentRegistry()

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    factory = registry.get_implementation_factory(
        "zn_hcl"
    )

    assert factory is DummyExperiment


def test_implementation_mapping_reject_duplicate():
    """
    Không cho phép đăng ký hai implementation
    cùng experiment_id.
    """

    registry = ExperimentRegistry()

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    with pytest.raises(ValueError):
        registry.register_implementation(
            "zn_hcl",
            AnotherDummyExperiment,
        )


def test_implementation_mapping_reject_invalid_factory():
    """
    Factory bắt buộc phải callable.
    """

    registry = ExperimentRegistry()

    with pytest.raises(TypeError):
        registry.register_implementation(
            "zn_hcl",
            "not a factory",
        )


# ============================================================
# 2. RESOLVER / FACTORY
# ============================================================

def test_create_implementation():
    """
    Registry phải tạo được implementation instance
    thông qua factory.
    """

    registry = ExperimentRegistry()

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    experiment = registry.create_implementation(
        "zn_hcl"
    )

    assert isinstance(
        experiment,
        DummyExperiment,
    )


def test_create_unknown_implementation():
    """
    Không tồn tại implementation mapping
    phải tạo lỗi rõ ràng.
    """

    registry = ExperimentRegistry()

    with pytest.raises(KeyError):
        registry.create_implementation(
            "unknown"
        )


# ============================================================
# 3. BUNDLE
# ============================================================

def test_resolve_returns_bundle():
    """
    resolve() phải trả về một ExperimentBundle.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle = registry.resolve(
        "zn_hcl"
    )

    assert bundle is not None
    assert hasattr(bundle, "definition")
    assert hasattr(bundle, "experiment")


def test_bundle_contains_definition():
    """
    Bundle phải chứa đúng ExperimentDefinition.
    """

    definition = create_definition()

    registry = ExperimentRegistry(
        definitions=[
            definition
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle = registry.resolve(
        "zn_hcl"
    )

    assert bundle.definition is definition


def test_bundle_contains_implementation():
    """
    Bundle phải chứa implementation instance.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle = registry.resolve(
        "zn_hcl"
    )

    assert isinstance(
        bundle.experiment,
        DummyExperiment,
    )


# ============================================================
# 4. ID CONSISTENCY
# ============================================================

def test_bundle_id_matches_definition():
    """
    Bundle.id phải khớp Definition.id.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle = registry.resolve(
        "zn_hcl"
    )

    assert bundle.id == "zn_hcl"
    assert bundle.id == bundle.definition.id


def test_bundle_rejects_mismatched_implementation():
    """
    Definition và implementation phải cùng experiment_id.
    """

    class WrongExperiment:
        id = "fe_hcl"

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        WrongExperiment,
    )

    with pytest.raises(ValueError):
        registry.resolve(
            "zn_hcl"
        )


# ============================================================
# 5. MISSING DEFINITION / IMPLEMENTATION
# ============================================================

def test_resolve_requires_definition():
    """
    Không có Definition thì resolve() không được
    tạo Bundle hoàn chỉnh.
    """

    registry = ExperimentRegistry()

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    with pytest.raises(KeyError):
        registry.resolve(
            "zn_hcl"
        )


def test_resolve_requires_implementation():
    """
    Có Definition nhưng không có implementation
    thì resolve() phải thất bại.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    with pytest.raises(KeyError):
        registry.resolve(
            "zn_hcl"
        )


# ============================================================
# 6. LIFECYCLE
# ============================================================

def test_resolve_creates_new_instance_each_time():
    """
    Mỗi lần resolve() phải tạo implementation
    instance mới.
    """

    registry = ExperimentRegistry(
        definitions=[
            create_definition()
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle_a = registry.resolve(
        "zn_hcl"
    )

    bundle_b = registry.resolve(
        "zn_hcl"
    )

    assert bundle_a.experiment is not bundle_b.experiment


def test_resolve_reuses_definition():
    """
    Definition có thể được dùng lại giữa
    nhiều lần resolve().
    """

    definition = create_definition()

    registry = ExperimentRegistry(
        definitions=[
            definition
        ]
    )

    registry.register_implementation(
        "zn_hcl",
        DummyExperiment,
    )

    bundle_a = registry.resolve(
        "zn_hcl"
    )

    bundle_b = registry.resolve(
        "zn_hcl"
    )

    assert bundle_a.definition is definition
    assert bundle_b.definition is definition