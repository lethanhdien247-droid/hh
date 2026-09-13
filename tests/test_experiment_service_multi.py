# ============================================================
# TEST EXPERIMENT SERVICE - MULTI EXPERIMENT
# tests/test_experiment_service_multi.py
# ============================================================

from experiments.registry import ExperimentRegistry
from experiments.zn_hcl import ZnHClExperiment
from services.experiment_service import ExperimentService


class DummyExperimentA:
    id = "dummy_a"
    name = "Mg + HCl"
    category = "Kim loại + axit"
    description = "Magie tác dụng với axit clohiđric."
    equation = "Mg + 2HCl → MgCl₂ + H₂"
    available = True

    def calculate(self, inputs):
        return None

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "equation": self.equation,
            "available": self.available,
        }


class DummyExperimentB:
    id = "dummy_b"
    name = "HCl + NaOH"
    category = "Axit + bazơ"
    description = "Axit clohiđric tác dụng với natri hiđroxit."
    equation = "HCl + NaOH → NaCl + H₂O"
    available = True

    def calculate(self, inputs):
        return None

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "equation": self.equation,
            "available": self.available,
        }


class DummyExperimentC:
    id = "dummy_c"
    name = "Fe + CuSO4"
    category = "Phản ứng thế"
    description = "Sắt tác dụng với đồng(II) sunfat."
    equation = "Fe + CuSO₄ → FeSO₄ + Cu"
    available = True

    def calculate(self, inputs):
        return None

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "equation": self.equation,
            "available": self.available,
        }


def create_multi_experiment_service():
    """
    Tạo Registry chứa nhiều Experiment để kiểm tra
    Service độc lập với số lượng Experiment.
    """
    registry = ExperimentRegistry()

    registry.register(DummyExperimentA())
    registry.register(DummyExperimentB())
    registry.register(DummyExperimentC())

    return ExperimentService(registry=registry)


def test_service_handles_multiple_experiments():
    service = create_multi_experiment_service()

    experiments = service.get_all_experiments()

    assert len(experiments) == 4

    ids = [experiment.id for experiment in experiments]

    assert ids == [
        "zn_hcl",
        "dummy_a",
        "dummy_b",
        "dummy_c",
    ]


def test_service_gets_each_experiment():
    service = create_multi_experiment_service()

    assert isinstance(
        service.get_experiment("zn_hcl"),
        ZnHClExperiment,
    )

    assert service.get_experiment("dummy_a").id == "dummy_a"
    assert service.get_experiment("dummy_b").id == "dummy_b"
    assert service.get_experiment("dummy_c").id == "dummy_c"


def test_service_returns_all_categories():
    service = create_multi_experiment_service()

    categories = service.get_categories()

    assert categories == [
        "Kim loại + axit",
        "Axit + bazơ",
        "Phản ứng thế",
    ]


def test_filter_returns_multiple_experiments():
    service = create_multi_experiment_service()

    results = service.filter_by_category(
        "Kim loại + axit"
    )

    assert len(results) == 2

    ids = [experiment.id for experiment in results]

    assert ids == [
        "zn_hcl",
        "dummy_a",
    ]


def test_filter_does_not_return_other_categories():
    service = create_multi_experiment_service()

    results = service.filter_by_category(
        "Axit + bazơ"
    )

    assert len(results) == 1
    assert results[0].id == "dummy_b"


def test_search_finds_by_id():
    service = create_multi_experiment_service()

    results = service.search_experiments("dummy_c")

    assert len(results) == 1
    assert results[0].id == "dummy_c"


def test_search_finds_by_name():
    service = create_multi_experiment_service()

    results = service.search_experiments("Mg + HCl")

    assert len(results) == 1
    assert results[0].id == "dummy_a"


def test_search_finds_multiple_results():
    service = create_multi_experiment_service()

    results = service.search_experiments("HCl")

    ids = [experiment.id for experiment in results]

    assert "zn_hcl" in ids
    assert "dummy_a" in ids
    assert "dummy_b" in ids

    assert len(results) == 3


def test_search_is_case_insensitive():
    service = create_multi_experiment_service()

    results = service.search_experiments("MG + HCL")

    assert len(results) == 1
    assert results[0].id == "dummy_a"


def test_search_by_description():
    service = create_multi_experiment_service()

    results = service.search_experiments(
        "đồng(II) sunfat"
    )

    assert len(results) == 1
    assert results[0].id == "dummy_c"


def test_unknown_search_returns_empty():
    service = create_multi_experiment_service()

    results = service.search_experiments(
        "phản ứng không tồn tại"
    )

    assert results == []


def test_empty_search_returns_all():
    service = create_multi_experiment_service()

    assert len(service.search_experiments("")) == 4
    assert len(service.search_experiments(None)) == 4


def test_empty_category_returns_all():
    service = create_multi_experiment_service()

    assert len(service.filter_by_category("")) == 4
    assert len(service.filter_by_category(None)) == 4


def test_unknown_category_returns_empty():
    service = create_multi_experiment_service()

    results = service.filter_by_category(
        "Không có category này"
    )

    assert results == []