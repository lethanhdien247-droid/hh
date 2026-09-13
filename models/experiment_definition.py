# ============================================================
# EXPERIMENT DEFINITION
# models/experiment_definition.py
# ============================================================


class ExperimentDefinition:
    """
    Data Model mô tả metadata của một thí nghiệm.

    ExperimentDefinition KHÔNG chứa logic hóa học.

    Nó chỉ đại diện cho:
        - id
        - name
        - category
        - description
        - equation
        - available
    """

    REQUIRED_FIELDS = (
        "id",
        "name",
        "category",
        "description",
        "equation",
        "available",
    )

    def __init__(
        self,
        id,
        name,
        category,
        description,
        equation,
        available,
    ):
        self.id = self._validate_string(
            id,
            "id",
        )

        self.name = self._validate_string(
            name,
            "name",
        )

        self.category = self._validate_string(
            category,
            "category",
        )

        self.description = self._validate_string(
            description,
            "description",
        )

        self.equation = self._validate_string(
            equation,
            "equation",
        )

        if not isinstance(available, bool):
            raise TypeError(
                "available must be a bool"
            )

        self.available = available

    # ========================================================
    # VALIDATION
    # ========================================================

    @staticmethod
    def _validate_string(
        value,
        field_name,
    ):
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string"
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty"
            )

        return value.strip()

    # ========================================================
    # SERIALIZATION
    # ========================================================

    def to_dict(self):
        """
        Chuyển Model thành dictionary.

        Dùng cho:
            - test
            - serialization
            - debugging
        """

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "equation": self.equation,
            "available": self.available,
        }

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self):
        return (
            "ExperimentDefinition("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"category={self.category!r}, "
            f"available={self.available!r}"
            ")"
        )