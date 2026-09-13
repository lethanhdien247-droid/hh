# ============================================================
# TEST EXPERIMENT DATA LOADER
# tests/test_experiment_data_loader.py
# ============================================================

import json

import pytest

from loaders.experiment_data_loader import (
    ExperimentDataLoader,
)
from models.experiment_definition import (
    ExperimentDefinition,
)


def test_load_zn_hcl():
    """
    Loader phải đọc được Zn + HCl từ JSON.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    definition = loader.load(
        "zn_hcl"
    )

    assert isinstance(
        definition,
        ExperimentDefinition,
    )

    assert definition.id == "zn_hcl"
    assert definition.name == "Zn + HCl"
    assert definition.category == "Kim loại + axit"
    assert definition.available is True


def test_loader_returns_definition_not_dict():
    """
    Loader phải trả về ExperimentDefinition,
    không phải dictionary.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    definition = loader.load(
        "zn_hcl"
    )

    assert isinstance(
        definition,
        ExperimentDefinition,
    )

    assert not isinstance(
        definition,
        dict,
    )


def test_loaded_definition_matches_json():
    """
    Metadata sau khi load phải giống JSON.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    definition = loader.load(
        "zn_hcl"
    )

    assert definition.to_dict() == {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": True,
    }


def test_unknown_experiment_raises_file_not_found():
    """
    Experiment không tồn tại phải báo FileNotFoundError.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        loader.load(
            "does_not_exist"
        )


def test_empty_experiment_id():
    """
    ID rỗng không hợp lệ.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    with pytest.raises(
        ValueError
    ):
        loader.load("")


def test_non_string_experiment_id():
    """
    ID phải là string.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    with pytest.raises(
        TypeError
    ):
        loader.load(123)


def test_path_traversal_is_rejected():
    """
    Không cho phép experiment_id chứa path.
    """

    loader = ExperimentDataLoader(
        "data/experiments"
    )

    with pytest.raises(
        ValueError
    ):
        loader.load(
            "../zn_hcl"
        )


def test_backslash_path_is_rejected():
    loader = ExperimentDataLoader(
        "data/experiments"
    )

    with pytest.raises(
        ValueError
    ):
        loader.load(
            "..\\zn_hcl"
        )


def test_missing_required_field(tmp_path):
    """
    JSON thiếu field bắt buộc phải bị từ chối.
    """

    data = {
        "id": "test",
        "name": "Test",
        "category": "Test",
        "description": "Test",
        "equation": "Test",

        # thiếu available
    }

    file_path = (
        tmp_path / "test.json"
    )

    file_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    loader = ExperimentDataLoader(
        tmp_path
    )

    with pytest.raises(
        ValueError
    ):
        loader.load("test")


def test_id_mismatch_is_rejected(tmp_path):
    """
    ID trong filename phải khớp ID trong JSON.
    """

    data = {
        "id": "wrong_id",
        "name": "Test",
        "category": "Test",
        "description": "Test",
        "equation": "Test",
        "available": True,
    }

    file_path = (
        tmp_path / "test.json"
    )

    file_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    loader = ExperimentDataLoader(
        tmp_path
    )

    with pytest.raises(
        ValueError
    ):
        loader.load("test")


def test_invalid_json(tmp_path):
    """
    JSON sai cú pháp phải bị phát hiện.
    """

    file_path = (
        tmp_path / "invalid.json"
    )

    file_path.write_text(
        "{ invalid json }",
        encoding="utf-8",
    )

    loader = ExperimentDataLoader(
        tmp_path
    )

    with pytest.raises(
        ValueError
    ):
        loader.load("invalid")


def test_json_root_must_be_object(tmp_path):
    """
    Root JSON phải là object/dict.
    """

    file_path = (
        tmp_path / "list.json"
    )

    file_path.write_text(
        json.dumps(
            [
                "zn_hcl"
            ]
        ),
        encoding="utf-8",
    )

    loader = ExperimentDataLoader(
        tmp_path
    )

    with pytest.raises(
        ValueError
    ):
        loader.load("list")


def test_custom_data_directory(tmp_path):
    """
    Loader phải hoạt động với data directory
    được truyền vào.
    """

    data = {
        "id": "test",
        "name": "Test",
        "category": "Test",
        "description": "Test experiment",
        "equation": "A → B",
        "available": False,
    }

    file_path = (
        tmp_path / "test.json"
    )

    file_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    loader = ExperimentDataLoader(
        tmp_path
    )

    definition = loader.load(
        "test"
    )

    assert definition.id == "test"
    assert definition.name == "Test"
    assert definition.available is False