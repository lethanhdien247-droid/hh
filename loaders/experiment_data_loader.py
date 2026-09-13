# ============================================================
# EXPERIMENT DATA LOADER
# loaders/experiment_data_loader.py
# ============================================================

import json
from pathlib import Path

from models.experiment_definition import ExperimentDefinition


class ExperimentDataLoader:
    """
    Đọc metadata Experiment từ file JSON.

    Data flow:

        JSON
         ↓
        ExperimentDataLoader
         ↓
        ExperimentDefinition

    Loader KHÔNG chịu trách nhiệm:
        - đăng ký Experiment
        - quản lý Registry
        - tính toán hóa học
        - ReactionEngine
        - UI
    """

    REQUIRED_FIELDS = {
        "id",
        "name",
        "category",
        "description",
        "equation",
        "available",
    }

    def __init__(self, data_directory):
        """
        Parameters
        ----------
        data_directory : str | Path
            Thư mục chứa các file JSON của Experiment.
        """

        self.data_directory = Path(
            data_directory
        )

    # ========================================================
    # LOAD ONE
    # ========================================================

    def load(self, experiment_id):
        """
        Đọc một Experiment từ file JSON.

        Ví dụ:

            loader.load("zn_hcl")

        sẽ đọc:

            data_directory / "zn_hcl.json"

        Returns
        -------
        ExperimentDefinition
        """

        file_path = self._get_file_path(
            experiment_id
        )

        data = self._read_json(
            file_path
        )

        self._validate_data(
            data,
            experiment_id,
        )

        return ExperimentDefinition(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            description=data["description"],
            equation=data["equation"],
            available=data["available"],
        )

    # ========================================================
    # FILE PATH
    # ========================================================

    def _get_file_path(self, experiment_id):
        """
        Tạo đường dẫn tới file JSON.

        Không cho phép experiment_id chứa path.
        """

        if not isinstance(
            experiment_id,
            str,
        ):
            raise TypeError(
                "experiment_id must be a string"
            )

        experiment_id = experiment_id.strip()

        if not experiment_id:
            raise ValueError(
                "experiment_id cannot be empty"
            )

        if (
            "/" in experiment_id
            or "\\" in experiment_id
            or experiment_id in {".", ".."}
        ):
            raise ValueError(
                "experiment_id must be a simple identifier"
            )

        return (
            self.data_directory
            / f"{experiment_id}.json"
        )

    # ========================================================
    # READ JSON
    # ========================================================

    @staticmethod
    def _read_json(file_path):
        """
        Đọc file JSON bằng UTF-8.
        """

        if not file_path.exists():
            raise FileNotFoundError(
                f"Experiment data file not found: "
                f"{file_path}"
            )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Experiment data path is not a file: "
                f"{file_path}"
            )

        try:
            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON file: {file_path}"
            ) from exc

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "Experiment JSON root must be an object"
            )

        return data

    # ========================================================
    # VALIDATION
    # ========================================================

    def _validate_data(
        self,
        data,
        experiment_id,
    ):
        """
        Kiểm tra contract của Experiment JSON.
        """

        missing_fields = (
            self.REQUIRED_FIELDS
            - set(data.keys())
        )

        if missing_fields:
            raise ValueError(
                "Missing required experiment fields: "
                + ", ".join(
                    sorted(missing_fields)
                )
            )

        if data["id"] != experiment_id:
            raise ValueError(
                "Experiment id does not match "
                "requested id"
            )