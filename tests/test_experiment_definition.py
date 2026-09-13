# ============================================================
# TEST EXPERIMENT DEFINITION
# tests/test_experiment_definition.py
# ============================================================

import pytest

from models.experiment_definition import (
    ExperimentDefinition,
)


def create_definition():
    return ExperimentDefinition(
        id="zn_hcl",
        name="Zn + HCl",
        category="Kim loại + axit",
        description="Kẽm tác dụng với axit clohiđric.",
        equation="Zn + 2HCl → ZnCl₂ + H₂",
        available=True,
    )


def test_create_experiment_definition():
    definition = create_definition()

    assert definition.id == "zn_hcl"
    assert definition.name == "Zn + HCl"
    assert definition.category == "Kim loại + axit"
    assert definition.description == (
        "Kẽm tác dụng với axit clohiđric."
    )
    assert definition.equation == (
        "Zn + 2HCl → ZnCl₂ + H₂"
    )
    assert definition.available is True


def test_to_dict():
    definition = create_definition()

    data = definition.to_dict()

    assert data == {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": True,
    }


def test_string_values_are_stripped():
    definition = ExperimentDefinition(
        id="  zn_hcl  ",
        name="  Zn + HCl  ",
        category="  Kim loại + axit  ",
        description="  Kẽm tác dụng với axit clohiđric.  ",
        equation="  Zn + 2HCl → ZnCl₂ + H₂  ",
        available=True,
    )

    assert definition.id == "zn_hcl"
    assert definition.name == "Zn + HCl"
    assert definition.category == "Kim loại + axit"
    assert definition.description == (
        "Kẽm tác dụng với axit clohiđric."
    )
    assert definition.equation == (
        "Zn + 2HCl → ZnCl₂ + H₂"
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", ""),
        ("name", ""),
        ("category", ""),
        ("description", ""),
        ("equation", ""),
    ],
)
def test_string_fields_cannot_be_empty(
    field,
    value,
):
    values = {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": True,
    }

    values[field] = value

    with pytest.raises(ValueError):
        ExperimentDefinition(**values)


@pytest.mark.parametrize(
    "field",
    [
        "id",
        "name",
        "category",
        "description",
        "equation",
    ],
)
def test_string_fields_must_be_strings(
    field,
):
    values = {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": True,
    }

    values[field] = 123

    with pytest.raises(TypeError):
        ExperimentDefinition(**values)


@pytest.mark.parametrize(
    "value",
    [
        None,
        "true",
        1,
        0,
        [],
        {},
    ],
)
def test_available_must_be_bool(value):
    values = {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": value,
    }

    with pytest.raises(TypeError):
        ExperimentDefinition(**values)


def test_available_can_be_false():
    values = {
        "id": "zn_hcl",
        "name": "Zn + HCl",
        "category": "Kim loại + axit",
        "description": "Kẽm tác dụng với axit clohiđric.",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "available": False,
    }

    definition = ExperimentDefinition(**values)

    assert definition.available is False


def test_repr():
    definition = create_definition()

    representation = repr(definition)

    assert "ExperimentDefinition" in representation
    assert "zn_hcl" in representation
    assert "Zn + HCl" in representation