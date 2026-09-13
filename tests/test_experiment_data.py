import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "experiments"
    / "zn_hcl.json"
)


def load_data():
    with DATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_zn_hcl_data_file_exists():
    assert DATA_FILE.exists()


def test_zn_hcl_data_is_valid_json():
    data = load_data()

    assert isinstance(data, dict)


def test_zn_hcl_data_has_required_fields():
    data = load_data()

    required_fields = {
        "id",
        "name",
        "category",
        "description",
        "equation",
        "available",
    }

    assert set(data.keys()) == required_fields


def test_zn_hcl_data_values():
    data = load_data()

    assert data["id"] == "zn_hcl"
    assert data["name"] == "Zn + HCl"
    assert data["category"] == "Kim loại + axit"
    assert data["description"] == (
        "Kẽm tác dụng với axit clohiđric."
    )
    assert data["equation"] == (
        "Zn + 2HCl → ZnCl₂ + H₂"
    )
    assert data["available"] is True


def test_zn_hcl_data_types():
    data = load_data()

    assert isinstance(data["id"], str)
    assert isinstance(data["name"], str)
    assert isinstance(data["category"], str)
    assert isinstance(data["description"], str)
    assert isinstance(data["equation"], str)
    assert isinstance(data["available"], bool)