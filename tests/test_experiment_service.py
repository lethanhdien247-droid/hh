# ============================================================
# TEST EXPERIMENT SERVICE
# tests/test_experiment_service.py
# ============================================================

from experiments.registry import ExperimentRegistry
from experiments.zn_hcl import ZnHClExperiment
from services.experiment_service import ExperimentService


def test_service_uses_default_registry():
    """Service phải tự hoạt động với Registry mặc định."""
    service = ExperimentService()

    experiments = service.get_all_experiments()

    assert len(experiments) == 1
    assert isinstance(experiments[0], ZnHClExperiment)


def test_get_all_experiments():
    """Service phải trả về toàn bộ Experiment."""
    service = ExperimentService()

    experiments = service.get_all_experiments()

    assert len(experiments) == 1
    assert experiments[0].id == "zn_hcl"


def test_get_experiment():
    """Service phải lấy Experiment theo id."""
    service = ExperimentService()

    experiment = service.get_experiment("zn_hcl")

    assert experiment is not None
    assert experiment.id == "zn_hcl"


def test_get_unknown_experiment():
    """ID không tồn tại phải trả về None."""
    service = ExperimentService()

    assert service.get_experiment("unknown") is None


def test_experiment_exists():
    """Service phải kiểm tra được Experiment tồn tại."""
    service = ExperimentService()

    assert service.experiment_exists("zn_hcl") is True
    assert service.experiment_exists("unknown") is False


def test_search_by_name():
    """Có thể tìm Experiment theo tên."""
    service = ExperimentService()

    results = service.search_experiments("Zn + HCl")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_search_case_insensitive():
    """Tìm kiếm không phân biệt hoa thường."""
    service = ExperimentService()

    results = service.search_experiments("zn + hcl")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_search_by_category():
    """Có thể tìm Experiment theo category."""
    service = ExperimentService()

    results = service.search_experiments("Kim loại + axit")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_search_by_description():
    """Có thể tìm Experiment theo description."""
    service = ExperimentService()

    results = service.search_experiments("clohiđric")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_search_empty_query_returns_all():
    """Query rỗng phải trả về toàn bộ Experiment."""
    service = ExperimentService()

    assert len(service.search_experiments("")) == 1
    assert len(service.search_experiments("   ")) == 1
    assert len(service.search_experiments(None)) == 1


def test_search_unknown_query_returns_empty():
    """Query không phù hợp phải trả về list rỗng."""
    service = ExperimentService()

    results = service.search_experiments("không tồn tại")

    assert results == []


def test_get_categories():
    """Service phải lấy được danh sách category duy nhất."""
    service = ExperimentService()

    categories = service.get_categories()

    assert categories == ["Kim loại + axit"]


def test_filter_by_category():
    """Service phải lọc Experiment theo category."""
    service = ExperimentService()

    results = service.filter_by_category("Kim loại + axit")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_filter_category_case_insensitive():
    """Lọc category không phân biệt hoa thường."""
    service = ExperimentService()

    results = service.filter_by_category("kim loại + AXIT")

    assert len(results) == 1
    assert results[0].id == "zn_hcl"


def test_filter_empty_category_returns_all():
    """Category rỗng phải trả về toàn bộ Experiment."""
    service = ExperimentService()

    assert len(service.filter_by_category("")) == 1
    assert len(service.filter_by_category("   ")) == 1
    assert len(service.filter_by_category(None)) == 1


def test_filter_unknown_category_returns_empty():
    """Category không tồn tại phải trả về list rỗng."""
    service = ExperimentService()

    results = service.filter_by_category("Không tồn tại")

    assert results == []


def test_service_dependency_injection():
    """
    Service phải có thể sử dụng Registry được truyền từ bên ngoài.
    """

    registry = ExperimentRegistry()
    service = ExperimentService(registry=registry)

    assert service.get_experiment("zn_hcl") is registry.get("zn_hcl")